from django.contrib import admin
from django.urls import (
    include,
    path,
)

urlpatterns = [
    path('', include('claypot.urls')),
    path('api/', include('claypot.api.urls')),
    path('admin/', admin.site.urls),
]
