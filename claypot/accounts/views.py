from django.contrib.auth import (
    login,
    logout
)

from .serializers import (
    LoginSerializer,
    UserSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)

from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

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
