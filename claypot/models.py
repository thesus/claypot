from django.conf import settings
from django.db import models
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
    instructions = models.TextField(
        verbose_name=ugettext_lazy('Instructions'))

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # Translators: author of recipe
        verbose_name=ugettext_lazy('Author'),
        related_name='authored_recipes',
    )
    published_on = models.DateTimeField(auto_now=True)
    starred_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='starred_recipes',
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
    def get_by_natural_key(self, recipe, ingredient):
        recipe = Recipe.objects.get_by_natural_key(*recipe)
        ingredient = Ingredient.objects.get_by_natural_key(*ingredient)
        return self.get(recipe=recipe, ingredient=ingredient)


class RecipeIngredient(models.Model):
    objects = RecipeIngredientManager()

    recipe = models.ForeignKey(
        'Recipe',
        verbose_name=ugettext_lazy('Recipe'),
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        verbose_name=ugettext_lazy('Ingredient'),
        on_delete=models.PROTECT,
        related_name='recipe_ingredients',
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
        related_name='recipe_ingredients',
    )

    def natural_key(self):
        return (
            self.recipe.natural_key(),
            self.ingredient.natural_key(),
        )

    def __str__(self):
        # Translators: Recipe ingredient display name
        return ugettext('{0.recipe}\'s {0.ingredient}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Recipe ingredient')
        verbose_name_plural = ugettext_lazy('Recipe ingredients')
        unique_together = ('recipe', 'ingredient')


class IngredientManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Ingredient(models.Model):
    objects = IngredientManager()

    name = models.CharField(
        max_length=200,
        verbose_name=ugettext_lazy('Name'),
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
