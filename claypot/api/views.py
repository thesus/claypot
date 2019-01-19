from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


class CsrfTokenView(View):
    def get(self, request):
        return HttpResponse('', content_type='text/plain')

csrf_token_view = ensure_csrf_cookie(CsrfTokenView.as_view())
