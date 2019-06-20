from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from claypot.accounts.tokens import signup_token_generator

from django.utils.translation import ugettext_lazy as _


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

    if settings.EMAIL_CONFIG.get("EMAIL_HOST_USER") and settings.EMAIL_CONFIG.get(
        "EMAIL_HOST"
    ):
        email_address = (
            settings.EMAIL_CONFIG["EMAIL_HOST_USER"]
            + settings.EMAIL_CONFIG["EMAIL_HOST"]
        )
    else:
        email_address = "webmaster@localhost"

    send_mail(
        _("E-Mail verification for {}".format(current_site.name)),
        email_body,
        email_address,
        [user.email],
    )
