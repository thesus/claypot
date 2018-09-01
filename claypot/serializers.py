from rest_framework import serializers

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Unit,
)

class NestedUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class NestedIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class NestedRecipeIngredientSerializer(serializers.ModelSerializer):
    unit = NestedUnitSerializer()
    ingredient = NestedIngredientSerializer()

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
            'title',
            'instructions',
            'recipe_ingredients',
        ]
