from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import serializers

from claypot.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeIngredientGroup,
    RecipeIngredientGroupIngredient,
    Unit,
)


class ManyIngredientSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(),
        min_length=0,
        max_length=20,
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
        return value and value.name

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
            'order',
            'ingredient',
            'ingredient_extra',
            'optional',
            'amount_type',
            'amount_numeric',
            'amount_approx',
            'unit',
        ]


class RecipeIngredientGroupIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientField()
    unit = UnitField()

    class Meta:
        model = RecipeIngredientGroupIngredient
        fields = [
            'order',
            'ingredient',
            'ingredient_extra',
            'optional',
            'amount_type',
            'amount_numeric',
            'amount_approx',
            'unit',
        ]


class RecipeIngredientGroupSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientGroupIngredientSerializer(many=True)

    class Meta:
        model = RecipeIngredientGroup
        fields = [
            'order',
            'title',
        ]


class UsernameField(serializers.RelatedField):
    def get_queryset(self):
        return get_user_model().objects.all()

    def to_representation(self, value):
        return value.username


class RecipeSerializer(serializers.ModelSerializer):
    author = UsernameField(required=False)
    ingredients = RecipeIngredientSerializer(many=True)
    ingredient_groups = RecipeIngredientGroupSerializer(many=True)
    is_starred = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()

    def get_is_starred(self, obj):
        return obj.starred_by.filter(pk=self.context['request'].user.id).exists()

    def get_stars(self, obj):
        return obj.starred_by.all().count()

    def create(self, validated_data):
        instance = Recipe(author=self.context['request'].user)
        return self.update(instance, validated_data)

    @method_decorator(transaction.atomic)
    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.slug = instance.slug or instance.title.lower().replace(' ', '-')
        instance.instructions = validated_data['instructions']
        instance.save()
        existing = set(ri.order for ri in instance.ingredients.all())
        new = set(ri['order'] for ri in validated_data['ingredients'])
        remove = existing - new
        instance.ingredients.filter(ingredient__in=remove).delete()
        for ri in validated_data['ingredients']:
            obj = instance.ingredients.filter(
                order=ri['order'],
            ).first()
            if obj is None:
                obj = RecipeIngredient(
                    recipe=instance,
                    order=ri['order'],
                )
            obj.ingredient = ri['ingredient']
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
            'ingredients',
            'ingredient_groups',
            'author',
            'author_id',
            'published_on',
            'is_starred',
            'stars',
        ]
        read_only_fields = [
            'id',
            'slug',
            'author',
            'author_id',
            'published_on',
            'starred_by',
            'is_starred',
            'stars',
        ]
