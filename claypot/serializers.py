from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Unit,
)


class IngredientRelatedField(serializers.RelatedField):
    slug_field = 'name'
    model = Ingredient
    queryset = Ingredient.objects.all()

    def to_internal_value(self, data):
        try:
            return self.queryset.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.model(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.slug_field)


class NestedRecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientRelatedField()
    unit = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Unit.objects.all(),
    )

    class Meta:
        model = RecipeIngredient
        fields = [
            'ingredient',
            'ingredient_extra',
            'optional',
            'amount_type',
            'amount_numeric',
            'amount_approx',
            'unit',
        ]


class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = NestedRecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'instructions',
            'recipe_ingredients',
        ]
