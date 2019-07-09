from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SentryConfigView, csrf_token_view
from .viewsets import (
    ImageViewSet,
    IngredientViewSet,
    RecipeViewSet,
    RecipeRelationViewSet,
)


router = DefaultRouter()
router.register("images", ImageViewSet)
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)
router.register("recipe_relations", RecipeRelationViewSet)

app_name = "api"
urlpatterns = [
    path("csrf", csrf_token_view),
    # Sentry configuration
    path("sentry", SentryConfigView.as_view(), name="sentry-config"),
    path("", include(router.urls)),
]
