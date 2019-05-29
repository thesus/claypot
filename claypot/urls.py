"""Define base urls here."""

from django.urls import path, include

from django.conf import settings

urlpatterns = [path("api/", include("claypot.api.urls"))]


if settings.DEBUG:
    from django.views.generic.base import TemplateView
    from django.conf.urls.static import static

    urlpatterns += [
        path("", TemplateView.as_view(template_name="index.html")),
        path("app.js", TemplateView.as_view(template_name="app.js")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
