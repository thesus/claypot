from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers

from claypot.accounts.utils import send_signup_mail

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = self.authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                msg = _("Account is disabled!")
                raise exceptions.ValidationError(msg)
        else:
            msg = _("Unable to login with provided credentials.")
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "email", "first_name", "last_name", "is_superuser")
        read_only_fields = ("email", "pk", "username")


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        self.form = PasswordResetForm(data=self.initial_data)
        if not self.form.is_valid():
            raise exceptions.ValidationError(self.form.errors)

        return value

    def save(self):
        request = self.context.get("request")

        options = {
            "use_https": request.is_secure(),
            "email_template_name": "accounts/password_reset_email.html",
            "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
            "request": request,
        }

        self.form.save(**options)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(
        max_length=128, style={"input_type": "password"}
    )
    new_password2 = serializers.CharField(
        max_length=128, style={"input_type": "password"}
    )

    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        # Try to get the user from the uid
        try:
            uid = force_text(urlsafe_base64_decode(attrs["uid"]))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            raise exceptions.ValidationError({"uid": ["Invalid value"]})

        self.form = SetPasswordForm(user=self.user, data=attrs)

        # Check if passwords ae valid
        if not self.form.is_valid():
            raise exceptions.ValidationError(self.form.errors)

        # Check token
        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise exceptions.ValidationError({"token": ["Invalid value"]})

        return attrs

    def save(self):
        return self.form.save()


class SignupSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=128, style={"input_type": "password"})
    password2 = serializers.CharField(max_length=128, style={"input_type": "password"})

    email = serializers.EmailField()
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            # Not sure if Django cares about lower and uppercase.
            User.objects.get(username__iexact=value)
        except User.DoesNotExist:
            return value
        raise exceptions.ValidationError(_("The username is already taken."))

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise exceptions.ValidationError(_("The email address is already used."))

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise exceptions.ValidationError(
                {"password2": [_("Passwords didn't match!")]}
            )

        return attrs

    def save(self):
        request = self.context.get("request")
        self.is_valid()

        user = User.objects.create_user(
            self.validated_data.get("username"),
            self.validated_data.get("email"),
            self.validated_data.get("password1"),
        )

        # Disabling user until email is verified
        user.is_active = False
        user.save()

        send_signup_mail(user, request)
