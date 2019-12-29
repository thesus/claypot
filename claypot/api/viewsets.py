from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from claypot.models import (
    Ingredient,
    IngredientSynonym,
    Recipe,
    RecipeDraft,
    RecipeRelation,
)

from .filters import IngredientFilter, RecipeFilter
from .permissions import ReadAllEditAdmin, ReadAllEditOwn, ReadOwnEditOwn
from .serializers import (
    IngredientSerializer,
    IngredientUpdateSerializer,
    ManyIngredientSerializer,
    RecipeDraftListSerializer,
    RecipeDraftSerializer,
    RecipeListSerializer,
    RecipeReadSerializer,
    RecipeRelationCreateSerializer,
    RecipeRelationSerializer,
    RecipeSerializer,
)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = [ReadAllEditAdmin]

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "update":
            return IngredientUpdateSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def check_new(self, request):
        serializer = ManyIngredientSerializer(data=request.data)
        if serializer.is_valid():
            requested = set(serializer.data["ingredients"])

            # Check in ingredients and synonyms
            existing = set(
                Ingredient.objects.filter(name__in=requested)
                .union(IngredientSynonym.objects.filter(name__in=requested))
                .values_list("name", flat=True)
            )

            new = list(requested - existing)
            return Response(ManyIngredientSerializer({"ingredients": new}).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("author").order_by("title").all()
    serializer_class = RecipeSerializer
    permission_classes = [ReadAllEditOwn]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if (
            self.action == "list"
            and self.request
            and self.request.method.lower() == "get"
        ):
            return RecipeListSerializer
        if (
            self.action == "retrieve"
            and self.request
            and self.request.method.lower() == "get"
        ):
            return RecipeReadSerializer
        return self.serializer_class

    @action(detail=True, methods=["post"])
    def star(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.starred_by.add(request.user)
        return Response(True)

    @action(detail=True, methods=["post"])
    def unstar(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.starred_by.remove(request.user)
        return Response(False)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @transaction.atomic
    def fork(self, request, pk=None):
        """Forks a existing recipe and sets a new owner."""

        def copy_foreign_key_relation(recipe, queryset):
            for instance in queryset:
                instance.pk = None
                instance.recipe = recipe
                instance.save()

        instance = get_object_or_404(Recipe, pk=pk)
        instance.parent_recipe = Recipe.objects.get(pk=pk)

        # Get all foreign key relationships
        # this has to be done here since they don't exist after saving the instance
        instructions = instance.instructions.all()
        images = instance.images.all()
        groups = instance.ingredients.all()

        instance.pk = None
        instance.slug = None
        instance.author = request.user
        instance.save()

        # Images are kind of immutable at the moment. They can't be deleted,
        # therefore they are simply copied to the fork.
        instance.images.set(images)

        for group in groups:
            ingredients = group.ingredients.all()
            group.pk = None
            group.recipe = instance
            group.save()
            for ingredient in ingredients:
                ingredient.pk = None
                ingredient.group = group
                ingredient.save()

        copy_foreign_key_relation(instance, instructions)

        return Response(instance.pk)

    def destroy(self, request, pk=None):
        obj = self.get_object()
        for i in obj.images.all():
            delete_image = False
            if not i.recipe_set.exclude(pk=obj.pk).exists():
                delete_image = True
            obj.images.remove(i)
            if delete_image:
                i.delete()
        return super().destroy(request, pk=pk)


class RecipeRelationViewSet(viewsets.ModelViewSet):
    queryset = RecipeRelation.objects.all().order_by("id")
    serializer_class = RecipeRelationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return RecipeRelationCreateSerializer
        else:
            return RecipeRelationSerializer

    def get_queryset(self):
        qs = self.queryset
        recipe = self.request.query_params.get("recipe")
        if recipe:
            qs = qs.filter(Q(recipe1_id=int(recipe)) | Q(recipe2_id=int(recipe)))
        return qs


class RecipeDraftViewSet(viewsets.ModelViewSet):
    queryset = RecipeDraft.objects.all().order_by("id")
    serializer_class = RecipeDraftSerializer
    permission_classes = [ReadOwnEditOwn]

    def get_serializer_class(self):
        if self.action == "list":
            return RecipeDraftListSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(
                recipe=None,
                author=self.request.user,
                date__gte=datetime.now() - timedelta(days=30),
            )
        else:
            return super().get_queryset()
