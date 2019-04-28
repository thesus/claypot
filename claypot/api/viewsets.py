from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from pytz import utc
from rest_framework import (
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters

from claypot.models import (
    Ingredient,
    Recipe,
)

from claypot.images.models import (
    Image,
)

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
    message = _('You may only edit your own recipes.')

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS) or
            request.user.is_authenticated or
            request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Recipe):
            if obj.author == request.user:
                if view.action != 'destroy':
                    return True
                else:
                    now = datetime.utcnow().replace(tzinfo=utc)
                    cut_off = now - settings.RECIPE_DELETE_GRACE_PERIOD
                    return obj.published_on > cut_off
        else:
            return False


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter

    @action(detail=False, methods=['post'])
    def create_many(self, request):
        serializer = IngredientSerializer(data=request.data, many=True)
        if serializer.is_valid():
            instances = serializer.save()
            return Response(
                IngredientSerializer(instances, many=True).data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_new(self, request):
        serializer = ManyIngredientSerializer(data=request.data)
        if serializer.is_valid():
            requested = set(serializer.data['ingredients'])
            existing = set(
                i.name
                for i in Ingredient.objects.filter(name__in=requested))
            new = list(requested - existing)
            return Response(
                ManyIngredientSerializer({"ingredients": new}).data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author_id = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
    )
    is_starred = django_filters.BooleanFilter(
        label='Is starred',
        method='filter_is_starred',
    )
    is_my_recipe = django_filters.BooleanFilter(
        label='Is my recipe',
        method='filter_is_my_recipe',
    )

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

    class Meta:
        model = Recipe
        fields = ['title']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [ReadAllEditOwn]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' and self.request.method.lower() == 'get':
            return RecipeListSerializer
        if self.action == 'retrieve' and self.request.method.lower() == 'get':
            return RecipeReadSerializer
        return self.serializer_class

    @action(detail=True, methods=['post'])
    def star(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.starred_by.add(request.user)
        return Response(True)

    @action(detail=True, methods=['post'])
    def unstar(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.starred_by.remove(request.user)
        return Response(False)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    @transaction.atomic
    def fork(self, request, pk=None):
        instance = get_object_or_404(Recipe, pk=pk)

        instance.parent_recipe = get_object_or_404(Recipe, pk=pk)

        recipe_ingredients = instance.ingredients.all()
        ingredient_groups = instance.ingredient_groups.all()

        instructions = instance.instructions.all()

        instance.pk = None
        instance.author = request.user
        instance.save()

        for group in ingredient_groups:
            ingredients = group.ingredients.all()
            group.pk = None
            group.recipe = instance
            group.save()
            for ingredient in ingredients:
                ingredient.pk = None
                ingredient.group = group
                ingredient.save()

        for ingredient in recipe_ingredients:
            ingredient.pk = None
            ingredient.recipe = instance
            ingredient.save()

        for instruction in instructions:
            instruction.pk = None
            instruction.recipe = instance
            instruction.save()

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
        if self.action == 'create':
            return ImageCreateSerializer
        else:
            return ImageRetrieveSerializer


    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Image()
        instance.save(**serializer.validated_data)

        return Response({'id': instance.pk})
