from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics
from rest_framework.response import Response


class CsrfTokenView(View):
    def get(self, request):
        return HttpResponse('', content_type='text/plain')

csrf_token_view = ensure_csrf_cookie(CsrfTokenView.as_view())


class SentryConfigView(generics.GenericAPIView):
    def get(self, request):
        return Response({
            'sentry_dsn': getattr(settings, 'SENTRY_PUBLIC_DSN', ''),
        })
