from rest_framework import viewsets

from claypot.models import (
    Ingredient,
    Recipe,
)

from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
