from rest_framework.routers import DefaultRouter

from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from claypot.api.viewsets import (
    IngredientViewSet,
    RecipeViewSet,
    RecipeRelationViewSet,
    RecipeDraftViewSet,
)

from claypot.api.views import SentryConfigView, csrf_token_view

from claypot.images.viewsets import ImageViewSet

from claypot.accounts.views import UserViewSet

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
    path("api/", include((router.urls, 'api'))),
    path("api/sentry", SentryConfigView.as_view(), name="sentry-config"),
    path("api/csrf", csrf_token_view),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    from django.views.generic.base import TemplateView
    from django.conf.urls.static import static

    urlpatterns += [
        path("", TemplateView.as_view(template_name="index.html")),
        path("app.js", TemplateView.as_view(template_name="app.js")),
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
