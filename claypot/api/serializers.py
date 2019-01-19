from rest_framework import serializers

from claypot.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Unit,
)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
        ]


class IngredientField(serializers.RelatedField):
    queryset = Ingredient.objects.all()

    def to_representation(self, value):
        return value.name


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            'id',
            'name',
            'name_plural',
            'code',
        ]


class UnitField(serializers.RelatedField):
    queryset = Unit.objects.all()

    def to_representation(self, value):
        return value.code


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientField()
    unit = UnitField()

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
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'slug',
            'instructions',
            'recipe_ingredients',
            'author',
            'published_on',
        ]
        read_only_fields = [
            'id',
            'slug',
            'author',
            'published_on',
            'starred_by',
        ]
