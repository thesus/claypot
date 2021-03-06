import operator
import uuid
from functools import reduce

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy


class UnitManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Unit(models.Model):
    objects = UnitManager()

    name = models.CharField(max_length=100, verbose_name=gettext_lazy("Name"))
    name_plural = models.CharField(
        max_length=100, verbose_name=gettext_lazy("Name, plural")
    )
    code = models.CharField(
        max_length=5,
        # Translators: Abbreviation for a unit
        verbose_name=gettext_lazy("Code"),
        blank=True,
    )

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        # Translators: Unit display name
        return gettext("{0.name}").format(self)

    class Meta:
        verbose_name = gettext_lazy("Unit")
        verbose_name_plural = gettext_lazy("Units")
        unique_together = ("name",)


RECIPE_RELATION_TYPE_ADDITION = 1
RECIPE_RELATION_TYPE_REPLACEMENT = 2
RECIPE_RELATION_TYPES = (
    (RECIPE_RELATION_TYPE_ADDITION, gettext_lazy("Addition")),
    (RECIPE_RELATION_TYPE_REPLACEMENT, gettext_lazy("Replacement")),
)


class RecipeRelation(models.Model):
    recipe1 = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="+")
    recipe2 = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="+")
    type = models.IntegerField(choices=RECIPE_RELATION_TYPES)

    class Meta:
        verbose_name = gettext_lazy("Recipe relation")
        verbose_name_plural = gettext_lazy("Recipe relations")
        unique_together = (("recipe1", "recipe2", "type"),)


class RecipeManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Recipe(models.Model):
    objects = RecipeManager()

    title = models.CharField(max_length=500, verbose_name=gettext_lazy("Title"))

    # Only used to load fixtures, otherwise filled with an uuid
    slug = models.SlugField(max_length=200)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # Translators: author of recipe
        verbose_name=gettext_lazy("Author"),
        related_name="authored_recipes",
    )
    published_on = models.DateTimeField(default=timezone.now)
    starred_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="starred_recipes"
    )
    images = models.ManyToManyField("images.Image")

    parent_recipe = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    estimated_work_duration = models.DurationField(
        null=True, verbose_name=gettext_lazy("Estimated time spent working")
    )
    estimated_waiting_duration = models.DurationField(
        null=True,
        verbose_name=gettext_lazy("Estimated waiting time"),
        help_text=gettext_lazy("Cooking and baking"),
    )
    related_recipes = models.ManyToManyField(
        "self", through=RecipeRelation, symmetrical=False, related_name="+"
    )
    description = models.TextField(
        blank=True, verbose_name=gettext_lazy("Additional information")
    )

    def save(self, *args, **kwargs):
        if not self.slug and not "slug" in kwargs:
            self.slug = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def tags(self):
        return set(
            IngredientTag.objects.filter(
                ingredients__instances__group__recipe=self
            ).distinct()
        )

    def is_starred_by(self, user):
        return self.starred_by.filter(pk=user.pk).exists()

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        # Translators: Recipe display name
        return gettext("{0.title}").format(self)

    class Meta:
        verbose_name = gettext_lazy("Recipe")
        verbose_name_plural = gettext_lazy("Recipes")
        unique_together = ("slug",)


AMOUNT_TYPE_NONE = 1
AMOUNT_TYPE_NUMERIC = 2
AMOUNT_TYPE_APPROX = 3
AMOUNT_TYPES = (
    (AMOUNT_TYPE_NONE, gettext_lazy("Unspecified amount")),
    (AMOUNT_TYPE_NUMERIC, gettext_lazy("Numeric amount")),
    (AMOUNT_TYPE_APPROX, gettext_lazy("Approximated amount")),
)


class RecipeIngredient(models.Model):
    """Stores an ingredient belonging to a group."""

    group = models.ForeignKey(
        "RecipeIngredientGroup", on_delete=models.CASCADE, related_name="ingredients"
    )

    order = models.IntegerField()

    ingredient = models.ForeignKey(
        "Ingredient",
        verbose_name=gettext_lazy("Ingredient"),
        on_delete=models.PROTECT,
        related_name="instances",
    )

    ingredient_extra = models.TextField(
        blank=True,
        # Translators: Optional field to note additional things about one
        # specific ingredient
        verbose_name=gettext_lazy("Additional notes about ingredient"),
    )

    optional = models.BooleanField(verbose_name=gettext_lazy("Optional"), default=False)

    amount_type = models.IntegerField(
        choices=AMOUNT_TYPES,
        # Translators: Name of internal field, e. g. "numeric amount",
        # "approximate amount"
        verbose_name=gettext_lazy("Amount type"),
        default=AMOUNT_TYPE_NUMERIC,
    )

    amount_numeric = models.FloatField(
        verbose_name=gettext_lazy("Amount, numeric"), null=True, blank=True
    )

    amount_approx = models.CharField(
        max_length=250,
        # Translators: Description of amount like "pint" or "some"
        verbose_name=gettext_lazy("Amount, approximated"),
        null=True,
        blank=True,
    )

    unit = models.ForeignKey(
        "Unit",
        on_delete=models.PROTECT,
        # Translators: Unit for a numeric amount
        verbose_name=gettext_lazy("Unit"),
        null=True,
        blank=True,
        related_name="+",
    )

    def natural_key(self):
        return (self.group.natural_key(), self.order)

    def __str__(self):
        # Translators: Recipe ingredient display name
        return gettext("{0.group.recipe}'s {0.ingredient}").format(self)

    class Meta:
        verbose_name = gettext_lazy("Recipe ingredient")
        verbose_name_plural = gettext_lazy("Recipe ingredients")
        unique_together = (("group", "order"),)


class RecipeIngredientGroupManager(models.Manager):
    def get_by_natural_key(self, recipe, order):
        recipe = Recipe.objects.get_by_natural_key(*recipe)
        return self.get(recipe=recipe, order=order)


class RecipeIngredientGroup(models.Model):
    objects = RecipeIngredientGroupManager()

    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="ingredients"
    )
    order = models.IntegerField()
    title = models.CharField(max_length=1000, blank=True)

    def natural_key(self):
        return (self.recipe.natural_key(), self.order)

    class Meta:
        verbose_name = gettext_lazy("Recipe ingredient group")
        verbose_name_plural = gettext_lazy("Recipe ingredient groups")
        unique_together = (("recipe", "order"),)


class IngredientSynonym(models.Model):
    name = models.CharField(max_length=200, verbose_name=gettext_lazy("Name"))
    ingredient = models.ForeignKey(
        "Ingredient", on_delete=models.CASCADE, related_name="synonyms"
    )

    class Meta:
        unique_together = ("name",)


class IngredientManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Ingredient(models.Model):
    objects = IngredientManager()

    name = models.CharField(max_length=200, verbose_name=gettext_lazy("Name"))
    tags = models.ManyToManyField("IngredientTag", related_name="ingredients")

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        # Translators: Ingredient display name
        return gettext("{0.name}").format(self)

    class Meta:
        verbose_name = gettext_lazy("Ingredient")
        verbose_name_plural = gettext_lazy("Ingredients")
        unique_together = ("name",)


class IngredientTagManager(models.Manager):
    def get_by_natural_key(self, tag):
        return self.get(tag=tag)


class IngredientTag(models.Model):
    objects = IngredientTagManager()

    tag = models.CharField(max_length=100)

    def natural_key(self):
        return (self.tag,)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = gettext_lazy("Tag")
        verbose_name_plural = gettext_lazy("Tags")
        unique_together = ("tag",)


class RecipeInstructionManager(models.Manager):
    def get_by_natural_key(self, recipe, order):
        recipe = Recipe.objects.get_by_natural_key(*recipe)
        return self.get(recipe=recipe, order=order)


class RecipeInstruction(models.Model):
    objects = RecipeInstructionManager()

    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="instructions"
    )
    order = models.IntegerField()
    text = models.TextField(blank=True)

    def natural_key(self):
        return (self.recipe.natural_key(), self.order)

    class Meta:
        verbose_name = gettext_lazy("Recipe instruction")
        verbose_name_plural = gettext_lazy("Recipe instructions")
        unique_together = ("recipe", "order")


class RecipeDraft(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Drafts don't have to have a recipe, they can be for new ones too.
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, blank=True, null=True, related_name="drafts"
    )

    # Recipe data is stored unverified as a json blob in the database.
    data = JSONField()

    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = gettext_lazy("Recipe draft")
        verbose_name_plural = gettext_lazy("Recipe drafts")
        ordering = ("id",)
        unique_together = ("author", "recipe")
