from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from .views import csrf_token_view
from .viewsets import (
    IngredientViewSet,
    RecipeViewSet,
)


router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('csrf', csrf_token_view),
    path('', include(router.urls)),
]
