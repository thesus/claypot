"""Define base urls here."""

from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('api/', include('claypot.api.urls')),
]


if settings.DEBUG:
    from django.views.generic.base import TemplateView
    from django.conf.urls.static import static

    urlpatterns += [
        path(
            '',
            TemplateView.as_view(template_name='index.html')
        )
    ] + static(
        '/',
        document_root=str(settings.ROOT_DIR.path('claypot/contrib'))
    )
