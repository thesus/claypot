from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import get_user_model, login, logout

from claypot.accounts.serializers import (
    LoginSerializer,
    UserSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    SignupSerializer,
)

from claypot.accounts.utils import send_signup_mail

from claypot.accounts.tokens import signup_token_generator, TimeoutError

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse

from rest_framework import permissions, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import action

from rest_framework.serializers import Serializer

User = get_user_model()


class ReadSelf(permissions.BasePermission):
    message = _("You may only view your own profile.")

    def has_permission(self, request, view):
        if view.action_map.get(request.method.lower(), None) == "retrieve":
            return request.user.is_authenticated or request.user.is_superuser
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action_map.get(request.method.lower(), None) == "retrieve":
            if request.method in permissions.SAFE_METHODS:
                if isinstance(obj, get_user_model()):
                    return obj == request.user
        return request.user.is_superuser


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        qs = get_user_model().objects.all()
        if not self.request.user.is_superuser:
            qs = qs.filter(pk=self.request.user.id)
        return qs

    serializer_class = UserSerializer

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
        uid = request.GET.get("uid", None)
        token = request.GET.get("token", None)

        # Decode user id to pk
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
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
