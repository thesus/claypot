from rest_framework.routers import DefaultRouter

from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from claypot.views import IndexView, RecipeDetailView
from claypot.api.viewsets import (
    IngredientViewSet,
    RecipeViewSet,
    RecipeRelationViewSet,
    RecipeDraftViewSet,
)

from claypot.api.views import SentryConfigView, csrf_token_view

from claypot.images.viewsets import ImageViewSet
from claypot.accounts.viewsets import UserViewSet

router = DefaultRouter()

views = (
    # api
    ("ingredients", IngredientViewSet),
    ("recipes", RecipeViewSet),
    ("recipe_relations", RecipeRelationViewSet),
    ("drafts", RecipeDraftViewSet),
    # images
    ("images", ImageViewSet),
    # accounts
    ("accounts", UserViewSet, "accounts"),
)

for view in views:
    router.register(*view)

urlpatterns = [
    path("", IndexView.as_view()),
    path("recipes/<int:pk>", RecipeDetailView.as_view()),
    path("api/", include((router.urls, "api"))),
    path("api/sentry", SentryConfigView.as_view(), name="sentry-config"),
    path("api/csrf", csrf_token_view),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    from django.views.generic.base import TemplateView
    from django.conf.urls.static import static

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(
        "js/", document_root=settings.APPS_DIR.path("templates", "claypot", "js")
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
