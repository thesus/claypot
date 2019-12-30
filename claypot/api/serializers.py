from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from pytz import utc
from rest_framework import serializers

from claypot.images.models import Image, ImageFile
from claypot.images.serializers import ImageRetrieveSerializer
from claypot.models import (
    AMOUNT_TYPES,
    RECIPE_RELATION_TYPE_REPLACEMENT,
    Ingredient,
    IngredientSynonym,
    IngredientTag,
    Recipe,
    RecipeDraft,
    RecipeIngredient,
    RecipeIngredientGroup,
    RecipeInstruction,
    RecipeRelation,
    Unit,
)


class OrderedListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by("order")
        return super().to_representation(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class ManyIngredientSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(min_length=0, max_length=100)
    )


class IngredientField(serializers.RelatedField):
    queryset = Ingredient.objects.all()

    def to_representation(self, value):
        return value and value.name

    @method_decorator(transaction.atomic)
    def to_internal_value(self, data):
        try:
            return Ingredient.objects.get(name=data)
        except Ingredient.DoesNotExist:
            try:
                return IngredientSynonym.objects.get(name=data).ingredient
            except IngredientSynonym.DoesNotExist:
                if not data:
                    serializers.ValidationError(_("This field may not be null."))
                else:
                    return Ingredient.objects.create(name=data)


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
            raise serializers.ValidationError(_("Unknown unit"))


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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ingredient = IngredientField()
    unit = UnitField()

    class Meta:
        model = RecipeIngredient
        list_serializer_class = OrderedListSerializer
        fields = [
            "id",
            "ingredient",
            "ingredient_extra",
            "optional",
            "amount_type",
            "amount_numeric",
            "amount_approx",
            "unit",
        ]


class RecipeIngredientGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = RecipeIngredientGroup
        list_serializer_class = OrderedListSerializer
        fields = ["id", "ingredients", "title"]


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


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientGroupSerializer(many=True)
    instructions = RecipeInstructionSerializer(many=True)
    images = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), many=True, allow_null=True
    )

    is_starred = serializers.SerializerMethodField()
    draft = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()
    deletable = serializers.SerializerMethodField()

    def get_draft(self, obj):
        if "request" in self.context and self.context["request"].user.is_authenticated:
            try:
                return obj.drafts.get(author=self.context["request"].user).pk
            except RecipeDraft.DoesNotExist:
                return None

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
        # save images
        if "images" in validated_data:
            existing = set(instance.images.values_list("id", flat=True))
            new = set(i.pk for i in validated_data.pop("images"))
            remove = existing - new

            instance.images.remove(*remove)
            instance.images.set(new)

        # save instructions
        if "instructions" in validated_data:
            instruction_data = validated_data.pop("instructions")
            existing = set(ri.order for ri in instance.instructions.all())
            new = set(ri["order"] for ri in instruction_data)

            remove = existing - new
            instance.instructions.filter(order__in=remove).delete()

            for ri in instruction_data:
                obj = instance.instructions.filter(order=ri["order"]).first()
                if obj is None:
                    obj = RecipeInstruction(recipe=instance, order=ri["order"])
                obj.text = ri["text"]
                obj.save()

        # Save new ingredients
        if "ingredients" in validated_data:
            ingredient_group_data = validated_data.pop("ingredients")

            existing = set(instance.ingredients.values_list("id", flat=True))
            current = set(
                ingredient["id"]
                for ingredient in ingredient_group_data
                if "id" in ingredient
            )
            instance.ingredients.filter(pk__in=existing - current).delete()

            for group_order, group_data in enumerate(ingredient_group_data):
                ingredients_data = group_data.pop("ingredients")

                if not "id" in group_data:
                    group = RecipeIngredientGroup.objects.create(
                        order=group_order, recipe=instance, **group_data
                    )
                    RecipeIngredient.objects.bulk_create(
                        RecipeIngredient(
                            group=group, order=ingredient_order, **ingredient_data
                        )
                        for (ingredient_order, ingredient_data) in enumerate(
                            ingredients_data
                        )
                    )
                else:
                    group, _ = instance.ingredients.get_or_create(
                        pk=group_data.pop("id"),
                        defaults={
                            "order": lambda: instance.ingredients.order_by(
                                "order"
                            ).last.order
                            + 1
                        },
                    )

                    group.title = group_data.pop("title")
                    group.save()

                    order = 0
                    for ingredient_data in ingredients_data:
                        ingredient_data["order"] = order
                        order += 1
                        group.ingredients.update_or_create(
                            pk=ingredient_data.pop("id", None),
                            defaults=ingredient_data,
                        )

        return super().update(instance, validated_data)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "instructions",
            "ingredients",
            "images",
            "author",
            "published_on",
            "draft",
            "deletable",
            "is_starred",
            "stars",
            "estimated_work_duration",
            "estimated_waiting_duration",
            "description",
        ]

        read_only_fields = [
            "author",
            "published_on",
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


class RecipeDraftSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RecipeDraft
        fields = ("id", "recipe", "data", "author")


class RecipeDraftListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = RecipeDraft
        fields = ("id", "date", "title")

    def get_title(self, obj):
        return obj.data.get("title", None)
