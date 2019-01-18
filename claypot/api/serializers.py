from rest_framework import serializers

from claypot.models import (
    Recipe,
    RecipeIngredient,
)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        exclude = []


class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = []
