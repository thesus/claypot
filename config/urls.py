from django.contrib import admin
from django.urls import (
    include,
    path,
)

urlpatterns = [
    path('api/', include('claypot.api.urls')),
    path('accounts/', include('claypot.accounts.urls')),

    path('admin/', admin.site.urls),
    path('', include('claypot.urls'))
]
