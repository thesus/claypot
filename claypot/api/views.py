from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from rest_framework import generics
from rest_framework.response import Response

from claypot import __version__


class CsrfTokenView(View):
    def get(self, request):
        return HttpResponse("", content_type="text/plain")


csrf_token_view = ensure_csrf_cookie(CsrfTokenView.as_view())


class SentryConfigView(generics.GenericAPIView):
    authentication_classes = []

    @method_decorator(cache_control(max_age=3600))
    def get(self, request):
        response = Response(
            {"sentry_dsn": getattr(settings, "SENTRY_FRONTEND_DSN", "")}
        )
        return response
