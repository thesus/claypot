from django.urls import (
    include,
    path
)
from rest_framework.routers import DefaultRouter

from claypot.accounts.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
    SignupConfirmView,
    SignupView,
    UserViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet, 'user')

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('reset', PasswordResetView.as_view()),
    path('confirm', PasswordResetConfirmView.as_view()),
    path('signup', SignupView.as_view()),
    path('activate/<uid>/<token>', SignupConfirmView.as_view(), name='activate'),
    path('', include(router.urls)),
]
