from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from .views import (
    SentryConfigView,
    csrf_token_view,
)
from .viewsets import (
    IngredientViewSet,
    RecipeViewSet,
    ImageViewSet
)


router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('images', ImageViewSet)

app_name = 'api'
urlpatterns = [
    path('csrf', csrf_token_view),

    # Sentry configuration
    path('sentry', SentryConfigView.as_view(), name='sentry-config'),

    path('', include(router.urls)),
]
