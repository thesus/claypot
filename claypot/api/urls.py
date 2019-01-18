from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from .viewsets import RecipeViewSet


router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
