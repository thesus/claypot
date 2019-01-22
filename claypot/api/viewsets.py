from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import (
    permissions,
    viewsets,
)
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from claypot.models import (
    Ingredient,
    Recipe,
)

from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
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
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Recipe):
            return obj.author == request.user
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


class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ['title']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [ReadAllEditOwn]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
