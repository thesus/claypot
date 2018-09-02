from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_starring(recipe_factory, user_factory, client):
    recipe = recipe_factory()
    assert recipe is not None
    user = user_factory()
    assert user is not None
    assert recipe.is_starred_by(user) is False
    client.force_login(user)
    url_starring = reverse(
        'recipe-set-star',
        kwargs={'pk': recipe.pk},
    )
    url_unstarring = reverse(
        'recipe-unset-star',
        kwargs={'pk': recipe.pk},
    )

    # Star recipe
    response = client.post(url_starring)
    assert response.status_code < 400
    recipe.refresh_from_db()
    assert recipe.is_starred_by(user) is True

    # Make sure nothing changes
    response = client.post(url_starring)
    assert response.status_code < 400
    recipe.refresh_from_db()
    assert recipe.is_starred_by(user) is True

    # Make sure it unstarrs
    response = client.post(url_unstarring)
    assert response.status_code < 400
    recipe.refresh_from_db()
    assert recipe.is_starred_by(user) is False

    # Make sure nothing changes
    response = client.post(url_unstarring)
    assert response.status_code < 400
    recipe.refresh_from_db()
    assert recipe.is_starred_by(user) is False
