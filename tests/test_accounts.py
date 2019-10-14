import pytest

from django.urls import reverse
from django.test import override_settings
from django.contrib.auth import authenticate


@pytest.mark.django_db
def test_login(api_client, django_user_model):
    """Tests the ability to login."""

    username = "user"
    password = "userpassword"

    user = django_user_model.objects.create_user(username=username, password=password)
    response = api_client.post(
        reverse("api:accounts-login"), {"username": username, "password": password}
    )

    # User should be redirected to the profile
    assert response.status_code == 302
    assert response.url == reverse("api:accounts-detail", kwargs={"pk": user.pk})

    # Try wrong password
    response = api_client.post(
        reverse("api:accounts-login"),
        {"username": username, "password": password + "_"},
    )
    assert response.status_code == 400

    # Disable user
    user.is_active = False
    user.save()
    response = api_client.post(
        reverse("api:accounts-login"), {"username": username, "password": password}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_account_permissions(api_client, user, admin_user):
    """Tests permission on profiles"""

    assert (
        api_client.get(
            reverse("api:accounts-detail", kwargs={"pk": user.pk})
        ).status_code
        == 403
    )

    # Users should only be able to see themselves
    api_client.force_login(user)
    assert (
        api_client.get(
            reverse("api:accounts-detail", kwargs={"pk": user.pk})
        ).status_code
        == 200
    )
    assert (
        api_client.get(
            reverse("api:accounts-detail", kwargs={"pk": admin_user.pk})
        ).status_code
        == 403
    )

    # Admins should be able to see all users
    api_client.force_login(admin_user)
    assert (
        api_client.get(
            reverse("api:accounts-detail", kwargs={"pk": user.pk})
        ).status_code
        == 200
    )


@pytest.mark.django_db
def test_logout(api_client, user):
    """Tests if users are logged out correctly."""

    api_client.force_login(user)

    assert "_auth_user_id" in api_client.session.keys()

    response = api_client.post(reverse("api:accounts-logout"))

    assert response.status_code == 200
    assert not "_auth_user_id" in api_client.session.keys()


@pytest.mark.django_db
def test_create_new_account(api_client, mailoutbox, django_user_model):
    """Tests creation of a new account."""

    response = api_client.post(
        reverse("api:accounts-signup"),
        {
            "password1": "password",
            "password2": "password",
            "username": "user",
            "email": "user@test.tld",
        },
    )

    user = django_user_model.objects.get(username="user")

    # Check email and extract link
    assert response.status_code == 200
    assert not user.is_active

    assert len(mailoutbox) == 1
    assert list(mailoutbox[0].to) == ["user@test.tld"]

    url = mailoutbox[0].body.splitlines()[7]

    # Activate account
    response = api_client.get(url)

    # Do query again, user changeqd
    user = django_user_model.objects.get(username="user")

    # Redirect to home page
    assert response.status_code == 302
    assert user.is_active

    # Link should be invalid by now
    response = api_client.get(url)
    assert response.status_code == 400


def test_invalid_account_links(api_client):
    """Tests if account activation can handle broken links."""

    # Run without token and uid parameters
    response = api_client.get(reverse("api:accounts-signup-confirm"))
    assert response.status_code == 400

    # Run with invalid token and uid
    response = api_client.get(
        reverse("api:accounts-signup-confirm") + "?token=bs&uid=r23"
    )
    assert response.status_code == 400


@override_settings(SIGNUP_TIMEOUT_DAYS=-1)
def test_expired_account_link(api_client, django_user_model, mailoutbox):
    """Tests if account activation renews activation link after the given timeout."""

    response = api_client.post(
        reverse("api:accounts-signup"),
        {
            "password1": "password",
            "password2": "password",
            "username": "user",
            "email": "user@test.tld",
        },
    )
    url = mailoutbox[0].body.splitlines()[7]

    response = api_client.get(url)

    assert response.status_code == 400
    # Link should be sent again in an email after clicking on the expired link.
    assert len(mailoutbox) == 2


@pytest.mark.django_db
def test_password_reset(api_client, user, mailoutbox):
    """Tests resetting of a user password."""

    user.email = "user@test.tld"
    user.save()

    response = api_client.post(reverse("api:accounts-reset"), {"email": user.email})

    assert response.status_code == 200
    assert len(mailoutbox) == 1

    uid, token = mailoutbox[0].body.splitlines()[7].split("/")[-2:]

    password = "apfelmus"
    response = api_client.post(
        reverse("api:accounts-reset-confirm"),
        {
            "token": token,
            "uid": uid,
            "new_password1": password,
            "new_password2": password,
        },
    )

    assert response.status_code == 200
    assert authenticate(username=user.username, password=password) is not None
