from rest_framework import serializers

from claypot.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Unit
)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = []


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        exclude = []


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()

    class Meta:
        model = RecipeIngredient
        exclude = []


class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = []
