import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_login(api_client, django_user_model):
    username = "user"
    password = "userpassword"

    user = django_user_model.objects.create_user(username=username, password=password)
    response = api_client.post(
        reverse("api:accounts-login"), {"username": username, "password": password}
    )

    # User should be redirected to the profile
    assert response.status_code == 302
    assert response.url == reverse("api:accounts-detail", kwargs={"pk": user.pk})


@pytest.mark.django_db
def test_account_permissions(api_client, user, admin_user):
    assert (
        api_client.get(
            reverse("api:accounts-detail", kwargs={"pk": user.pk})
        ).status_code
        == 403
    )

    # Users should only see themselves
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
    api_client.force_login(user)

    assert "_auth_user_id" in api_client.session.keys()

    response = api_client.post(reverse("api:accounts-logout"))

    assert response.status_code == 200
    assert not "_auth_user_id" in api_client.session.keys()


@pytest.mark.django_db
def test_create_new_account(api_client, mailoutbox, django_user_model):
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


@pytest.mark.django_db
def test_password_reset(api_client, user, mailoutbox):
    user.email = "user@test.tld"
    user.save()

    response = api_client.post(reverse("api:accounts-reset"), {"email": user.email})

    assert response.status_code == 200
    assert len(mailoutbox) == 1
