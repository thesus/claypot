from django.urls import (
    include,
    path
)

from .views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView
)


urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('reset', PasswordResetView.as_view()),
    path('confirm', PasswordResetConfirmView.as_view())
]
