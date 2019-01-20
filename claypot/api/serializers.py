from django.contrib.auth import get_user_model
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

    def to_internal_value(self, data):
        try:
            return Ingredient.objects.get(name=data)
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError('Unknown ingredient')


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

    def to_internal_value(self, data):
        try:
            return Unit.objects.get(code=data)
        except Unit.DoesNotExist:
            raise serializers.ValidationError('Unknown unit')


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

class UsernameField(serializers.RelatedField):
    def get_queryset(self):
        return get_user_model().objects.all()

    def to_representation(self, value):
        return value.username


class RecipeSerializer(serializers.ModelSerializer):
    author = UsernameField(required=False)
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    def create(self, validated_data):
        instance = Recipe(author=self.context['request'].user)
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.slug = instance.slug or instance.title.lower().replace(' ', '-')
        instance.instructions = validated_data['instructions']
        instance.save()
        existing = set(ri.ingredient for ri in instance.recipe_ingredients.all())
        new = set(ri['ingredient'] for ri in validated_data['recipe_ingredients'])
        remove = existing - new
        instance.recipe_ingredients.filter(ingredient__in=remove).delete()
        for ri in validated_data['recipe_ingredients']:
            obj = instance.recipe_ingredients.filter(ingredient=ri['ingredient']).first()
            if obj is None:
                obj = RecipeIngredient(recipe=instance, ingredient=ri['ingredient'])
            obj.ingredient_extra = ri['ingredient_extra']
            obj.optional = ri['optional']
            obj.amount_type = ri['amount_type']
            obj.amount_numeric = ri['amount_numeric']
            obj.amount_approx = ri['amount_approx']
            obj.unit = ri['unit']
            obj.save()
        return instance

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'slug',
            'instructions',
            'recipe_ingredients',
            'author',
            'author_id',
            'published_on',
        ]
        read_only_fields = [
            'id',
            'slug',
            'author',
            'author_id',
            'published_on',
            'starred_by',
        ]
