from django.conf import settings

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("claypot.api.urls", namespace="claypot.api")),
    path("accounts/", include("claypot.accounts.urls")),
    path("admin/", admin.site.urls),
    path("", include("claypot.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
