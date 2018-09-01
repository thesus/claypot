from django.conf import settings
from django.db import models
from django.utils.translation import (
    ugettext,
    ugettext_lazy
)


class Unit(models.Model):
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

    def __str__(self):
        # Translators: Unit display name
        return ugettext('{0.name}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Unit')
        verbose_name_plural = ugettext_lazy('Units')


class Recipe(models.Model):
    title = models.CharField(
        max_length=500,
        verbose_name=ugettext_lazy('Title'),
    )
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

    def __str__(self):
        # Translators: Recipe display name
        return ugettext('{0.name}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Recipe')
        verbose_name_plural = ugettext_lazy('Recipes')


AMOUNT_TYPE_NONE = 1
AMOUNT_TYPE_NUMERIC = 2
AMOUNT_TYPE_APPROX = 3
AMOUNT_TYPES = (
    (AMOUNT_TYPE_NONE, ugettext_lazy('Unspecified amount')),
    (AMOUNT_TYPE_NUMERIC, ugettext_lazy('Numeric amount')),
    (AMOUNT_TYPE_APPROX, ugettext_lazy('Approximated amount')),
)


class RecipeIngredient(models.Model):
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
    )
    amount_approx = models.CharField(
        max_length=250,
        # Translators: Description of amount like "pint" or "some"
        verbose_name=ugettext_lazy('Amount, approximated'),
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

    def __str__(self):
        # Translators: Recipe ingredient display name
        return ugettext('{0.recipe}\'s {0.ingredient}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Recipe ingredient')
        verbose_name_plural = ugettext_lazy('Recipe ingredients')


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=ugettext_lazy('Name'),
    )

    def __str__(self):
        # Translators: Ingredient display name
        return ugettext('{0.name}').format(self)

    class Meta:
        verbose_name = ugettext_lazy('Ingredient')
        verbose_name_plural = ugettext_lazy('Ingredients')
