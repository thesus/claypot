from datetime import datetime
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from pytz import utc

from django.db.models import prefetch_related_objects

from claypot.models import (
    AMOUNT_TYPES,
    AbstractIngredient,
    Ingredient,
    IngredientSynonym,
    IngredientTag,
    RECIPE_RELATION_TYPE_REPLACEMENT,
    Recipe,
    RecipeIngredient,
    RecipeIngredientGroup,
    RecipeIngredientGroupIngredient,
    RecipeInstruction,
    RecipeRelation,
    Unit,
)

from claypot.images.models import Image, ImageFile


class OrderedListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by("order")
        return super().to_representation(data)


class ImageCreateSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ["image_file", "height", "width"]
        read_only_fields = ["image_file", "height", "width"]


class ImageRetrieveSerializer(serializers.ModelSerializer):
    files = ImageFileSerializer(many=True)
    thumbnail = ImageFileSerializer()

    class Meta:
        model = Image
        fields = ["id", "files", "thumbnail"]
        read_only_fields = ["id", "files"]


class ImageThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = ImageFileSerializer()

    class Meta:
        model = Image
        fields = ["thumbnail"]
        read_only_fields = ["thumbnail"]


class ManyIngredientSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(), min_length=0, max_length=100
    )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class IngredientField(serializers.RelatedField):
    queryset = Ingredient.objects.all()

    def to_representation(self, value):
        return value and value.name

    def to_internal_value(self, data):
        try:
            return Ingredient.objects.get(name=data)
        except Ingredient.DoesNotExist:
            try:
                return IngredientSynonym.objects.get(name=data).ingredient
            except IngredientSynonym.DoesNotExist:
                raise serializers.ValidationError("Unknown ingredient")


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name", "name_plural", "code"]


class UnitField(serializers.RelatedField):
    queryset = Unit.objects.all()

    def run_validation(self, *args, **kwargs):
        # This is required, because RelatedField sets empty strings to None.
        # The best way to avoid this seems to be skipping it and directly
        # calling its ancestor, Field.
        return serializers.Field.run_validation(self, *args, **kwargs)

    def to_representation(self, value):
        return value.code

    def to_internal_value(self, data):
        try:
            return Unit.objects.get(code=data)
        except Unit.DoesNotExist:
            raise serializers.ValidationError("Unknown unit")


class UsernameField(serializers.RelatedField):
    def get_queryset(self):
        return get_user_model().objects.all()

    def to_representation(self, value):
        return value.username


class RecipeInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInstruction
        list_serializer_class = OrderedListSerializer
        fields = ["order", "text"]


class RecipeIngredientSerializer(serializers.Serializer):
    ingredient = IngredientField()
    ingredient_extra = serializers.CharField(allow_blank=True)
    optional = serializers.BooleanField()
    amount_type = serializers.ChoiceField(choices=AMOUNT_TYPES)
    amount_numeric = serializers.FloatField(allow_null=True)
    amount_approx = serializers.CharField(allow_null=True, allow_blank=True)
    unit = UnitField()


class RecipeIngredientListSerializer(serializers.Serializer):
    is_group = serializers.BooleanField()
    title = serializers.CharField(allow_blank=True)
    ingredients = RecipeIngredientSerializer(many=True)


class RecipeListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ["id", "title", "thumbnail"]

    def get_thumbnail(self, obj):
        image = obj.images.first()
        if image and image.thumbnail and image.thumbnail.image_file:
            return self.context["request"].build_absolute_uri(
                image.thumbnail.image_file.url
            )
        return None


class RecipeSerializer(serializers.Serializer):
    id = serializers.ModelField(
        model_field=Recipe._meta.get_field("id"), read_only=True
    )
    title = serializers.ModelField(model_field=Recipe._meta.get_field("title"))
    slug = serializers.ModelField(
        model_field=Recipe._meta.get_field("slug"), read_only=True
    )
    author_id = serializers.ModelField(
        model_field=Recipe._meta.get_field("author_id"), read_only=True
    )
    published_on = serializers.ModelField(
        model_field=Recipe._meta.get_field("published_on"), read_only=True
    )
    author = UsernameField(required=False)
    parent_recipe = serializers.ModelField(
        model_field=Recipe._meta.get_field("parent_recipe"), read_only=True
    )
    estimated_work_duration = serializers.ModelField(
        model_field=Recipe._meta.get_field("estimated_work_duration"), allow_null=True
    )
    estimated_waiting_duration = serializers.ModelField(
        model_field=Recipe._meta.get_field("estimated_waiting_duration"),
        allow_null=True,
    )

    images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)

    instructions = RecipeInstructionSerializer(many=True)
    is_starred = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()
    deletable = serializers.SerializerMethodField()

    def to_representation(self, recipe):
        data = super().to_representation(recipe)
        ingredients = []

        if recipe.ingredients.exists():
            ingredients.append(
                RecipeIngredientListSerializer(
                    {
                        "is_group": False,
                        "title": "",
                        "ingredients": recipe.ingredients.order_by("order")
                        .prefetch_related("ingredient", "unit")
                        .all(),
                    }
                ).data
            )

        for group in recipe.ingredient_groups.all():
            group_ingredients = (
                group.ingredients.prefetch_related("ingredient")
                .prefetch_related("unit")
                .order_by("order")
                .all()
            )

            ingredients.append(
                RecipeIngredientListSerializer(
                    {
                        "is_group": True,
                        "title": group.title,
                        "ingredients": group_ingredients,
                    }
                ).data
            )

        data["ingredients"] = ingredients
        return data

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        sub_serializer = RecipeIngredientListSerializer(
            data=data["ingredients"], many=True
        )
        if not sub_serializer.is_valid():
            raise serializers.ValidationError({"ingredients": sub_serializer.errors})
        value["ingredients"] = sub_serializer.validated_data
        return value

    def get_is_starred(self, obj):
        if "request" in self.context:
            return obj.starred_by.filter(pk=self.context["request"].user.id).exists()
        else:
            return None

    def get_stars(self, obj):
        return obj.starred_by.all().count()

    def get_deletable(self, obj):
        if "request" in self.context:
            request = self.context["request"]
            user = request.user
            if user.is_superuser or user.is_staff:
                return True
            elif obj.author == request.user:
                now = datetime.utcnow().replace(tzinfo=utc)
                cut_off = now - settings.RECIPE_DELETE_GRACE_PERIOD
                return obj.published_on > cut_off
            else:
                return False
        else:
            return False

    def create(self, validated_data):
        instance = Recipe(author=self.context["request"].user)
        return self.update(instance, validated_data)

    @method_decorator(transaction.atomic)
    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.estimated_work_duration = validated_data["estimated_work_duration"]
        instance.estimated_waiting_duration = validated_data[
            "estimated_waiting_duration"
        ]
        instance.save()

        # save images
        existing = set(instance.images.values_list("id", flat=True))

        new = set(i.pk for i in validated_data["images"])
        remove = existing - new

        instance.images.remove(*remove)
        instance.images.set(new)

        # save instructions
        existing = set(ri.order for ri in instance.instructions.all())
        new = set(ri["order"] for ri in validated_data["instructions"])
        remove = existing - new
        instance.instructions.filter(order__in=remove).delete()
        for ri in validated_data["instructions"]:
            obj = instance.instructions.filter(order=ri["order"]).first()
            if obj is None:
                obj = RecipeInstruction(recipe=instance, order=ri["order"])
            obj.text = ri["text"]
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
        for grp in validated_data["ingredients"]:
            relevant_order = order
            if grp["is_group"] is True:
                pk = {"recipe": instance, "order": order}
                values = {"title": grp["title"]}
                complete_ref = (order,)
                if complete_ref in existing:
                    existing_obj = existing[complete_ref]
                    del existing[complete_ref]
                    if not isinstance(existing_obj, RecipeIngredientGroup):
                        existing_obj.delete()
                        rig = RecipeIngredientGroup.objects.create(**pk, **values)
                    else:
                        RecipeIngredientGroup.objects.filter(pk=existing_obj.pk).update(
                            **values
                        )
                    rig = RecipeIngredientGroup.objects.get(**pk)
                else:
                    rig = RecipeIngredientGroup.objects.create(**pk, **values)
                relevant_order = 1
                ref = (order,)
                order += 1
                cls = RecipeIngredientGroupIngredient
                parent_ref = {"group": rig}
            else:
                ref = ()
                order += len(grp["ingredients"])
                cls = RecipeIngredient
                parent_ref = {"recipe": instance}
            for ingredient in grp["ingredients"]:
                pk = {"order": relevant_order}
                pk.update(parent_ref)
                values = {
                    "ingredient": ingredient["ingredient"],
                    "ingredient_extra": ingredient["ingredient_extra"],
                    "optional": ingredient["optional"],
                    "amount_type": ingredient["amount_type"],
                    "amount_numeric": ingredient["amount_numeric"],
                    "amount_approx": ingredient["amount_approx"],
                    "unit": ingredient["unit"],
                }
                # import pdb
                # pdb.set_trace()
                complete_ref = ref + (relevant_order,)
                if complete_ref in existing:
                    existing_obj = existing[complete_ref]
                    del existing[complete_ref]
                    if not isinstance(existing_obj, cls):
                        existing_obj.delete()
                        cls.objects.create(**pk, **values)
                    else:
                        cls.objects.filter(pk=existing_obj.pk).update(**values)
                else:
                    cls.objects.create(**pk, **values)
                relevant_order += 1
        for i in existing.values():
            i.delete()

        return instance

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "slug",
            "instructions",
            "ingredients",
            "ingredient_groups",
            "images",
            "author",
            "author_id",
            "published_on",
            "is_starred",
            "stars",
            "estimated_work_duration",
            "estimated_waiting_duration",
        ]
        read_only_fields = [
            "id",
            "slug",
            "author",
            "author_id",
            "published_on",
            "starred_by",
            "is_starred",
            "stars",
        ]


class RecipeReadSerializer(RecipeSerializer):
    images = ImageRetrieveSerializer(read_only=True, many=True)


class ManySynonymSerializer(serializers.Serializer):
    synonyms = serializers.ListField(
        child=serializers.CharField(), min_length=0, max_length=100
    )


class SlugCreateRelatedField(serializers.SlugRelatedField):
    """Takes a model and returns a unsaved model instance if it does'nt exist."""

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.model(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail("invalid")


class IngredientUpdateSerializer(serializers.ModelSerializer):
    synonyms = SlugCreateRelatedField(
        many=True,
        queryset=IngredientSynonym.objects.all(),
        model=IngredientSynonym,
        slug_field="name",
    )

    tags = SlugCreateRelatedField(
        many=True,
        queryset=IngredientTag.objects.all(),
        model=IngredientTag,
        slug_field="tag",
    )

    @transaction.atomic
    def save(self):
        def get_error(i):
            return serializers.ValidationError(
                {"synonyms": {i: [_("Already used on another ingredient.")]}}
            )

        ingredient = self.instance

        # Save new tags
        for tag in self.validated_data["tags"]:
            if not tag.pk:
                tag.save()

        # Set all tags on ingredient
        ingredient.tags.set(self.validated_data["tags"])

        updated = set()
        for i, synonym in enumerate(self.validated_data["synonyms"]):
            # Save new synonyms and add them to new set
            if not synonym.pk:
                synonym.ingredient = ingredient
                try:
                    synonym.save()
                except IntegrityError:
                    raise get_error(i)
            else:
                # Synonym needs to be unique to one ingredient
                if synonym.ingredient != ingredient:
                    raise get_error(i)

            updated.add(synonym.pk)

        # Delete unmentioned synonyms
        ingredient.synonyms.exclude(pk__in=updated).delete()

        # Add tags and synonyms from equivalent ingredients
        ingredients = Ingredient.objects.filter(
            name__in=[i.name for i in self.validated_data["synonyms"]]
        )
        for synonymous_ingredient in ingredients:
            ingredient.tags.add(*synonymous_ingredient.tags.all())

            # Add synonyms from synonymous ingredient to the 'correct' ingredient
            synonymous_ingredient.synonyms.update(ingredient=ingredient)

            # Update ingredients in recipes
            RecipeIngredient.objects.filter(ingredient=synonymous_ingredient).update(
                ingredient=ingredient
            )
            RecipeIngredientGroupIngredient.objects.filter(
                ingredient=synonymous_ingredient
            ).update(ingredient=ingredient)
        ingredients.delete()

    class Meta:
        model = Ingredient
        fields = ["name", "synonyms", "tags"]
        read_only_fields = ["name"]


class RecipeRelationSerializer(serializers.ModelSerializer):
    recipe1 = RecipeListSerializer()
    recipe2 = RecipeListSerializer()

    class Meta:
        model = RecipeRelation
        fields = ("id", "recipe1", "recipe2", "type")


class RecipeRelationCreateSerializer(serializers.ModelSerializer):
    recipe1 = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    recipe2 = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    def save(self):
        recipe1 = self.validated_data["recipe1"]
        recipe2 = self.validated_data["recipe2"]

        if recipe1 == recipe2:
            return serializers.ValidationError(
                {
                    "recipe1": {
                        i: [
                            _(
                                "You may only define relations between different recipes."
                            )
                        ]
                    }
                }
            )

        return RecipeRelation.objects.filter(
            (Q(recipe1=recipe1) & Q(recipe2=recipe2))
            | (Q(recipe1=recipe2) & Q(recipe2=recipe1))
        ).get_or_create(self.validated_data)[0]

    class Meta:
        model = RecipeRelation
        fields = ("id", "recipe1", "recipe2", "type")
