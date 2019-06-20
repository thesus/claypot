from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, get_language_info
from django_filters.rest_framework import DjangoFilterBackend
from pytz import utc
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import django_filters

from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)

from claypot.models import Ingredient, Recipe
from claypot.images.models import Image

from .serializers import (
    ImageCreateSerializer,
    ImageRetrieveSerializer,
    IngredientSerializer,
    ManyIngredientSerializer,
    RecipeSerializer,
    RecipeListSerializer,
    RecipeReadSerializer,
)


class ReadAllEditOwn(permissions.BasePermission):
    message = _("You may only edit your own recipes.")

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or request.user.is_authenticated
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Recipe):
            if obj.author == request.user:
                if view.action != "destroy":
                    return True
                else:
                    now = datetime.utcnow().replace(tzinfo=utc)
                    cut_off = now - settings.RECIPE_DELETE_GRACE_PERIOD
                    return obj.published_on > cut_off
        else:
            return False


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ["name"]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter

    @action(detail=False, methods=["post"])
    def create_many(self, request):
        serializer = IngredientSerializer(data=request.data, many=True)
        if serializer.is_valid():
            instances = serializer.save()
            return Response(IngredientSerializer(instances, many=True).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def check_new(self, request):
        serializer = ManyIngredientSerializer(data=request.data)
        if serializer.is_valid():
            requested = set(serializer.data["ingredients"])
            existing = set(
                i.name for i in Ingredient.objects.filter(name__in=requested)
            )
            new = list(requested - existing)
            return Response(ManyIngredientSerializer({"ingredients": new}).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    author_id = django_filters.ModelChoiceFilter(
        field_name="author", queryset=User.objects.all()
    )
    is_starred = django_filters.BooleanFilter(
        label="Is starred", method="filter_is_starred"
    )
    is_my_recipe = django_filters.BooleanFilter(
        label="Is my recipe", method="filter_is_my_recipe"
    )
    search = django_filters.CharFilter(label="Search", method="search_filter")

    def filter_is_starred(self, queryset, name, value):
        if value is True:
            if self.request.user.pk is not None:
                return queryset.filter(starred_by__id=self.request.user.pk)
            else:
                # anonymous
                return queryset.none()
        if value is False:
            if self.request.user.pk is not None:
                return queryset.exclude(starred_by__id=self.request.user.pk)
            else:
                # anonymous
                return queryset
        return queryset

    def filter_is_my_recipe(self, queryset, name, value):
        if value is True:
            if self.request.user.pk is not None:
                return queryset.filter(author=self.request.user)
            else:
                # anonymous
                return queryset.none()
        if value is False:
            if self.request.user.pk is not None:
                return queryset.exclude(author=self.request.user)
            else:
                # anonymous
                return queryset
        return queryset

    def search_filter(self, queryset, name, value):
        if value:
            # Build search vector containing the following fields:
            # - title
            # - instructions
            # - ingredients (group/non group)
            vector = (
                SearchVector("title", weight="A")
                + SearchVector(
                    StringAgg("instructions__text", delimiter=" "), weight="C"
                )
                + SearchVector(
                    StringAgg("ingredients__ingredient__name", delimiter=" "),
                    weight="B",
                )
                + SearchVector(
                    StringAgg(
                        "ingredient_groups__ingredients__ingredient__name",
                        delimiter=" ",
                    ),
                    weight="B",
                )
            )

            # extract language in lowercase for postgres tsquery
            lang = get_language_info(get_language())["name"].lower()
            query = SearchQuery(value, config=lang)

            # Query based on vector search and trigram similarity
            queryset = (
                queryset.annotate(
                    rank=SearchRank(vector, query),
                    similarity=TrigramSimilarity("title", value),
                )
                .filter(Q(rank__gte=0.1) | Q(similarity__gt=0.1))
                .order_by("-rank")
            )
            return queryset
        else:
            return queryset

    class Meta:
        model = Recipe
        fields = ["title"]


class RecipePagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = "page_size"
    max_page_size = 100


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("author").order_by("title").all()
    serializer_class = RecipeSerializer
    permission_classes = [ReadAllEditOwn]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.action == "list" and self.request.method.lower() == "get":
            return RecipeListSerializer
        if self.action == "retrieve" and self.request.method.lower() == "get":
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
        instance.slug = None

        # Get all foreign key relationships
        recipe_ingredients = instance.ingredients.all()
        ingredient_groups = instance.ingredient_groups.all()
        instructions = instance.instructions.all()
        images = instance.images.all()

        instance.pk = None
        instance.author = request.user
        instance.save()

        # Images are kind of immutable at the moment. They can't be deleted,
        # therefore they are simply copied to the fork.
        instance.images.set(images)

        for group in ingredient_groups:
            ingredients = group.ingredients.all()
            group.pk = None
            group.recipe = instance
            group.save()
            for ingredient in ingredients:
                ingredient.pk = None
                ingredient.group = group
                ingredient.save()

        copy_foreign_key_relation(instance, recipe_ingredients)
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


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = [ReadAllEditOwn]

    def get_serializer_class(self):
        if self.action == "create":
            return ImageCreateSerializer
        else:
            return ImageRetrieveSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Image()
        instance.save(**serializer.validated_data)

        return Response({"id": instance.pk})
