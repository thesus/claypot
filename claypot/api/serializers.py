from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import serializers

from claypot.models import (
    AMOUNT_TYPES,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeIngredientGroup,
    RecipeIngredientGroupIngredient,
    RecipeInstruction,
    Unit,
)


class OrderedListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('order')
        return super().to_representation(data)


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


class UsernameField(serializers.RelatedField):
    def get_queryset(self):
        return get_user_model().objects.all()

    def to_representation(self, value):
        return value.username


class RecipeInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInstruction
        list_serializer_class = OrderedListSerializer
        fields = [
            'order',
            'text',
        ]


class RecipeIngredientSerializer(serializers.Serializer):
    ingredient = IngredientField()
    ingredient_extra = serializers.CharField(allow_blank=True)
    optional = serializers.BooleanField()
    amount_type = serializers.ChoiceField(choices=AMOUNT_TYPES)
    amount_numeric = serializers.FloatField()
    amount_approx = serializers.CharField(allow_null=True, allow_blank=True)
    unit = UnitField()


class RecipeIngredientListSerializer(serializers.Serializer):
    is_group = serializers.BooleanField()
    title = serializers.CharField(allow_blank=True)
    ingredients = RecipeIngredientSerializer(many=True)


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title']


class RecipeSerializer(serializers.Serializer):
    id = serializers.ModelField(
        model_field=Recipe._meta.get_field('id'), read_only=True)
    title = serializers.ModelField(
        model_field=Recipe._meta.get_field('title'))
    slug = serializers.ModelField(
        model_field=Recipe._meta.get_field('slug'), read_only=True)
    author_id = serializers.ModelField(
        model_field=Recipe._meta.get_field('author_id'), read_only=True)
    published_on = serializers.ModelField(
        model_field=Recipe._meta.get_field('published_on'), read_only=True)
    author = UsernameField(required=False)
    instructions = RecipeInstructionSerializer(many=True)
    is_starred = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()

    def to_representation(self, recipe):
        data = super().to_representation(recipe)
        ingredients = (
            set(recipe.ingredients.all()) |
            set(recipe.ingredient_groups.all()))
        all_ingredients = sorted(ingredients, key=lambda i: i.order)
        ingredients = []
        buf = []
        def _flush():
            ingredients.append(
                RecipeIngredientListSerializer({
                    'is_group': False,
                    'title': '',
                    'ingredients': buf,
                }).data)
            buf.clear()

        for i in all_ingredients:
            if isinstance(i, RecipeIngredient):
                buf.append(i)
            else:
                if len(buf) > 0:
                    _flush()
                ingredients.append(
                    RecipeIngredientListSerializer({
                        'is_group': True,
                        'title': i.title,
                        'ingredients': i.ingredients.all().order_by('order'),
                    }).data)
        if len(buf) > 0:
            _flush()
        data['ingredients'] = ingredients
        return data

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        sub_serializer = RecipeIngredientListSerializer(data=data['ingredients'], many=True)
        if not sub_serializer.is_valid():
            raise serializers.ValidationError({'ingredients': sub_serializer.errors})
        value['ingredients'] = sub_serializer.validated_data
        return value

    def get_is_starred(self, obj):
        if 'request' in self.context:
            return obj.starred_by.filter(pk=self.context['request'].user.id).exists()
        else:
            return None

    def get_stars(self, obj):
        return obj.starred_by.all().count()

    def create(self, validated_data):
        instance = Recipe(author=self.context['request'].user)
        return self.update(instance, validated_data)

    @method_decorator(transaction.atomic)
    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.slug = instance.slug or instance.title.lower().replace(' ', '-')
        instance.save()

        print(validated_data)
        # save instructions
        existing = set(ri.order for ri in instance.instructions.all())
        new = set(ri['order'] for ri in validated_data['instructions'])
        remove = existing - new
        instance.instructions.filter(order__in=remove).delete()
        for ri in validated_data['instructions']:
            obj = instance.instructions.filter(
                order=ri['order'],
            ).first()
            if obj is None:
                obj = RecipeInstruction(
                    recipe=instance,
                    order=ri['order'],
                )
            obj.text = ri['text']
            obj.save()

        # save ingredients
        order = 1
        existing = {}
        for i in instance.ingredients.all():
            existing[i.order,] = i
        for grp in instance.ingredient_groups.all():
            existing[grp.order,] = grp
            for i in grp.ingredients.all():
                existing[grp.order, i.order] = i
        for grp in validated_data['ingredients']:
            relevant_order = order
            if grp['is_group'] is True:
                pk = {
                    "recipe": instance,
                    "order": order,
                }
                values = {
                    "title": grp['title'],
                }
                complete_ref = (order,)
                if complete_ref in existing:
                    existing_obj = existing[complete_ref]
                    if not isinstance(existing_obj, RecipeIngredientGroup):
                        existing_obj.delete()
                        rig = RecipeIngredientGroup.objects.create(**pk, **values)
                    else:
                        RecipeIngredientGroup.objects.filter(pk=existing_obj.pk).update(**values)
                    rig = RecipeIngredientGroup.objects.get(**pk)
                else:
                    rig = RecipeIngredientGroup.objects.create(**pk, **values)
                relevant_order = 1
                ref = (order,)
                order += 1
                cls = RecipeIngredientGroupIngredient
                parent_ref = {'group': rig}
            else:
                ref = ()
                order += len(grp['ingredients'])
                cls = RecipeIngredient
                parent_ref = {'recipe': instance}
            for ingredient in grp['ingredients']:
                pk = {
                    "order": relevant_order,
                }
                pk.update(parent_ref)
                values = {
                    "ingredient": ingredient['ingredient'],
                    "ingredient_extra": ingredient['ingredient_extra'],
                    "optional": ingredient['optional'],
                    "amount_type": ingredient['amount_type'],
                    "amount_numeric": ingredient['amount_numeric'],
                    "amount_approx": ingredient['amount_approx'],
                    "unit": ingredient['unit'],
                }
                #import pdb
                #pdb.set_trace()
                complete_ref = ref + (relevant_order,)
                if complete_ref in existing:
                    existing_obj = existing[complete_ref]
                    if not isinstance(existing_obj, cls):
                        existing_obj.delete()
                        cls.objects.create(**pk, **values)
                    else:
                        cls.objects.filter(pk=existing_obj.pk).update(**values)
                else:
                    cls.objects.create(**pk, **values)
                relevant_order += 1

        return instance
