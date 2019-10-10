from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, mixins

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from claypot.accounts.serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    SignupSerializer,
    UserSerializer,
)
from claypot.accounts.tokens import TimeoutError, signup_token_generator
from claypot.accounts.utils import send_signup_mail

from .permissions import ReadSelf


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_permissions(self):
        if self.action in ("retrieve",):
            return (ReadSelf(),)
        else:
            return ()

    @action(detail=False, methods=["post"], serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)

        # Redirect to user profile after succesfull login
        return redirect(reverse("api:accounts-detail", kwargs={"pk": user.pk}))

    @action(detail=False, methods=["post"], serializer_class=Serializer)
    def logout(self, request):
        logout(request)

        return Response({"detail": _("Logged out successfully.")})

    @action(detail=False, methods=["post"], serializer_class=PasswordResetSerializer)
    def reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"detail": _("Reset email has been sent.")})

    @action(
        detail=False, methods=["post"], serializer_class=PasswordResetConfirmSerializer
    )
    def reset_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"detail": _("Password resetted successfully.")})

    @action(detail=False, methods=["post"], serializer_class=SignupSerializer)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"detail": _("Signup email has been sent.")})

    @action(detail=False, methods=["get"], serializer_class=Serializer)
    def signup_confirm(self, request):
        """login"""

        uid = request.GET.get("uid")
        token = request.GET.get("token")

        if not uid or not token:
            return HttpResponse(_("Signup link is missing get parameters!"))

        # Decode user id to pk
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid)
        except (get_user_model().DoesNotExist, TypeError, ValueError, OverflowError):
            return HttpResponse(
                _("Signup link is invalid. Did you copy the URL correctly?")
            )

        # Check if the token is valid
        # if the token is invalidated due to being too old, a new mail will be sent.
        try:
            if not signup_token_generator.check_token(user, token):
                return HttpResponse(_("Signup link is invalid!"))
        except TimeoutError:
            send_signup_mail(user, request)
            return HttpResponse(
                _("Signup link no longer valid. New email has been sent.")
            )

        user.is_active = True
        user.save()

        return redirect("/#/accounts/login")
