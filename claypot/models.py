from functools import reduce
import operator

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import (
    ugettext,
    ugettext_lazy
)


class UnitManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Unit(models.Model):
    objects = UnitManager()

    name = models.CharField(
        max_length=100,
        verbose_name=ugettext_lazy('Name'),
    )
    name_plural = models.CharField(
        max_length=100,
        verbose_name=ugettext_lazy('Name, plural'),
    )
    code = models.CharField(
        max_length=5,
        # Translators: Abbreviation for a unit
        verbose_name=ugettext_lazy('Code'),
        blank=True,
    )

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        # Translators: Unit display name
        return ugettext('{0.name}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Unit')
        verbose_name_plural = ugettext_lazy('Units')
        unique_together = ('name',)


class RecipeManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Recipe(models.Model):
    objects = RecipeManager()

    title = models.CharField(
        max_length=500,
        verbose_name=ugettext_lazy('Title'),
    )
    slug = models.SlugField(max_length=200)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # Translators: author of recipe
        verbose_name=ugettext_lazy('Author'),
        related_name='authored_recipes',
    )
    published_on = models.DateTimeField(default=timezone.now)
    starred_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='starred_recipes',
    )

    def tags(self):
        return reduce(
            operator.or_,
            (set(ri.ingredient.tags.all())
                for ri in self.ingredients.all()),
            set()
        )

    def is_starred_by(self, user):
        return self.starred_by.filter(pk=user.pk).exists()

    def natural_key(self):
        return (self.slug,)

    def __str__(self):
        # Translators: Recipe display name
        return ugettext('{0.title}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Recipe')
        verbose_name_plural = ugettext_lazy('Recipes')
        unique_together = ('slug',)


AMOUNT_TYPE_NONE = 1
AMOUNT_TYPE_NUMERIC = 2
AMOUNT_TYPE_APPROX = 3
AMOUNT_TYPES = (
    (AMOUNT_TYPE_NONE, ugettext_lazy('Unspecified amount')),
    (AMOUNT_TYPE_NUMERIC, ugettext_lazy('Numeric amount')),
    (AMOUNT_TYPE_APPROX, ugettext_lazy('Approximated amount')),
)


class RecipeIngredientManager(models.Manager):
    def get_by_natural_key(self, recipe, order):
        recipe = Recipe.objects.get_by_natural_key(*recipe)
        return self.get(recipe=recipe, order=order)


class AbstractIngredient(models.Model):
    objects = RecipeIngredientManager()

    ingredient = models.ForeignKey(
        'Ingredient',
        verbose_name=ugettext_lazy('Ingredient'),
        on_delete=models.PROTECT,
        related_name='+',
    )

    ingredient_extra = models.TextField(
        blank=True,
        # Translators: Optional field to note additional things about one specific
        # ingredient
        verbose_name=ugettext_lazy('Additional notes about ingredient'),
    )
    optional = models.BooleanField(
        verbose_name=ugettext_lazy('Optional'),
        default=False,
    )
    amount_type = models.IntegerField(
        choices=AMOUNT_TYPES,
        # Translators: Name of internal field, e. g. "numeric amount",
        # "approximate amount"
        verbose_name=ugettext_lazy('Amount type'),
        default=AMOUNT_TYPE_NUMERIC,
    )
    amount_numeric = models.FloatField(
        verbose_name=ugettext_lazy('Amount, numeric'),
        null=True,
        blank=True,
    )
    amount_approx = models.CharField(
        max_length=250,
        # Translators: Description of amount like "pint" or "some"
        verbose_name=ugettext_lazy('Amount, approximated'),
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        'Unit',
        on_delete=models.PROTECT,
        # Translators: Unit for a numeric amount
        verbose_name=ugettext_lazy('Unit'),
        null=True,
        blank=True,
        related_name='+',
    )

    def natural_key(self):
        return (self.recipe.natural_key(), self.order)

    def __str__(self):
        # Translators: Recipe ingredient display name
        return ugettext('{0.recipe}\'s {0.ingredient}').format(self)

    class Meta:
        abstract = True
        verbose_name = ugettext_lazy('Recipe ingredient')
        verbose_name_plural = ugettext_lazy('Recipe ingredients')


class RecipeIngredient(AbstractIngredient):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    order = models.IntegerField()

    class Meta:
        verbose_name = ugettext_lazy('Recipe ingredient')
        verbose_name_plural = ugettext_lazy('Recipe ingredients')
        unique_together = ('recipe', 'order')


class RecipeIngredientGroupManager(models.Manager):
    def get_by_natural_key(self, recipe, order):
        recipe = Recipe.objects.get_by_natural_key(*recipe)
        return self.get(recipe=recipe, order=order)


class RecipeIngredientGroup(models.Model):
    objects = RecipeIngredientGroupManager()

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredient_groups',
    )
    order = models.IntegerField()
    title = models.CharField(max_length=1000)

    def natural_key(self):
        return (
            self.recipe.natural_key(),
            self.order,
        )

    class Meta:
        verbose_name = ugettext_lazy('Recipe ingredient group')
        verbose_name_plural = ugettext_lazy('Recipe ingredient groups')
        unique_together = ('recipe', 'order')


class RecipeIngredientGroupIngredientManager(models.Manager):
    def get_by_natural_key(self, group, order):
        group = RecipeIngredientGroup.objects.get_by_natural_key(*group)
        return self.get(group=group, order=order)


class RecipeIngredientGroupIngredient(AbstractIngredient):
    objects = RecipeIngredientGroupIngredientManager()

    group = models.ForeignKey(
        'RecipeIngredientGroup',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    order = models.IntegerField()

    def natural_key(self):
        return (self.group.natural_key(), self.order)

    class Meta:
        verbose_name = ugettext_lazy('Recipe ingredient group ingredient')
        verbose_name_plural = ugettext_lazy('Recipe ingredient group ingredients')
        unique_together = ('group', 'order')


class IngredientManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Ingredient(models.Model):
    objects = IngredientManager()

    name = models.CharField(
        max_length=200,
        verbose_name=ugettext_lazy('Name'),
    )
    tags = models.ManyToManyField(
        'IngredientTag',
        related_name='ingredients',
    )

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        # Translators: Ingredient display name
        return ugettext('{0.name}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Ingredient')
        verbose_name_plural = ugettext_lazy('Ingredients')
        unique_together = ('name',)


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
        verbose_name = ugettext_lazy('Tag')
        verbose_name_plural = ugettext_lazy('Tags')
        unique_together = ('tag',)


class RecipeInstructionManager(models.Manager):
    def get_by_natural_key(self, recipe, order):
        recipe = Recipe.objects.get_by_natural_key(*recipe)
        return self.get(recipe=recipe, order=order)


class RecipeInstruction(models.Model):
    objects = RecipeInstructionManager()

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='instructions',
    )
    order = models.IntegerField()
    text = models.TextField(blank=True)

    def natural_key(self):
        return (
            self.recipe.natural_key(),
            self.order,
        )

    class Meta:
        verbose_name = ugettext_lazy('Recipe instruction')
        verbose_name_plural = ugettext_lazy('Recipe instructions')
        unique_together = ('recipe', 'order')
