from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from claypot.accounts.tokens import signup_token_generator


def send_signup_mail(user, request):
    current_site = get_current_site(request)

    email_body = render_to_string(
        "accounts/signup_email.html",
        {
            "token": signup_token_generator.make_token(user),
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "domain": current_site.domain,
            "site_name": current_site.name,
            "user": user,
            "protocol": "https" if request.is_secure() else "http",
        },
    )

    # Django environ counts the @-character as part of the user
    email_address = (settings.EMAIL_CONFIG.get("EMAIL_HOST_USER") or "webmaster@") + (
        settings.EMAIL_CONFIG.get("EMAIL_HOST") or "localhost"
    )

    send_mail(
        _("E-Mail verification for {}").format(current_site.name),
        email_body,
        email_address,
        [user.email],
    )
