from rest_framework import serializers

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Unit,
)


class NestedRecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all(),
    )
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
            'title',
            'instructions',
            'recipe_ingredients',
        ]
