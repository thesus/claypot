from django.urls import (
    include,
    path
)

from claypot.accounts.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    SignupView,
    SignupConfirmView
)


urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('reset', PasswordResetView.as_view()),
    path('confirm', PasswordResetConfirmView.as_view()),
    path('signup', SignupView.as_view()),
    path('activate/<uid>/<token>', SignupConfirmView.as_view(), name='activate')
]
