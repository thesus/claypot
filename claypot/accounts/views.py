from django.shortcuts import redirect

from django.contrib.auth import (
    login,
    logout,
    get_user_model
)

from claypot.accounts.serializers import (
    LoginSerializer,
    UserSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    SignupSerializer
)

from claypot.accounts.utils import (
    signup_token_generator
)

from django.views import View

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

User = get_user_model()

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def perform_login(self):
        user = self.serializer.validated_data['user']
        login(self.request, user)

    def get_response(self):
        serializer = UserSerializer(
            instance=self.serializer.validated_data['user']
        )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        self.request = request

        self.serializer = self.get_serializer(
            data=request.data
        )

        self.serializer.is_valid(raise_exception=True)
        self.perform_login()

        return self.get_response()


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        self.request = request
        logout(request)

        return Response({'detail': _("Logged out successfully.")})

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'detail': _("Reset email has been sent.")
        })


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'detail': _("Password resetted successfully.")
        })

class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'detail': _("Signup email has been sent.")
        })

class SignupConfirmView(View):
    def get(self, request, uid, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            return Response({
                'detail': _("Signup link is invalid. Have copied it wrong?")
            })
        
        if not signup_token_generator.check_token(user, token):
            return Response({
                'detail': _("Signup link is invalid!")
            })
        
        user.is_active = True
        user.save()

        return redirect("/#/accounts/login")
