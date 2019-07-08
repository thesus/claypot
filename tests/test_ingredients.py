import pytest

from django.urls import reverse
from rest_framework import status

from claypot.models import Ingredient


@pytest.mark.django_db
def test_synonym_merging(api_client, ingredient_factory, ingredient_tag_factory, user):
    ingredient_a = ingredient_factory()
    ingredient_b = ingredient_factory()

    user.is_superuser = True
    user.save()

    api_client.force_login(user)
    response = api_client.put(
        reverse("api:ingredient-detail", kwargs={"pk": ingredient_a.pk}),
        {"synonyms": [ingredient_b.name, "test"]},
    )

    assert response.status_code == status.HTTP_200_OK
    assert ingredient_a.synonyms.count() == 2
    assert Ingredient.objects.all().count() == 1
