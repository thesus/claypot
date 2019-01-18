from rest_framework import viewsets

from claypot.models import Recipe

from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
