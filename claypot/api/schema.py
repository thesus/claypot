from graphene import relay, ObjectType, Schema
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from claypot.models import (
    Ingredient,
    IngredientTag,
    Recipe,
    RecipeIngredient,
    Unit,
)


class IngredientNode(DjangoObjectType):

    class Meta:
        model = Ingredient
        filter_fields = [
            'name',
            'tags',
        ]
        interfaces = (relay.Node,)


class IngredientTagNode(DjangoObjectType):
    class Meta:
        model = IngredientTag
        filter_fields = [
            'tag',
        ]
        interfaces = (relay.Node,)


class RecipeNode(DjangoObjectType):
    class Meta:
        model = Recipe
        filter_fields = {
            'title': ['exact', 'icontains'],
            'slug': ['exact', 'icontains'],
            'instructions': ['icontains'],
            'author': ['exact'],
            'published_on': ['exact', 'lte', 'gte'],
        }
        interfaces = (relay.Node,)


class RecipeIngredientNode(DjangoObjectType):
    class Meta:
        model = RecipeIngredient
        interfaces = (relay.Node,)


class UnitNode(DjangoObjectType):
    class Meta:
        model = Unit
        filter_fields = [
            'name',
        ]
        interfaces = (relay.Node,)


class Query(ObjectType):
    ingredient = relay.Node.Field(IngredientNode)
    ingredients = DjangoFilterConnectionField(IngredientNode)
    ingredient_tag = relay.Node.Field(IngredientTagNode)
    ingredient_tags = DjangoFilterConnectionField(IngredientTagNode)
    recipe = relay.Node.Field(RecipeNode)
    recipes = DjangoFilterConnectionField(RecipeNode)
    unit = relay.Node.Field(UnitNode)
    units = DjangoFilterConnectionField(UnitNode)


schema = Schema(query=Query)
