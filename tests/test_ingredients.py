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


@pytest.mark.django_db
def test_check_new(api_client, ingredient_factory, user):
    api_client.force_login(user)
    ingredient1 = ingredient_factory()
    ingredient2 = ingredient_factory()

    url = reverse("api:ingredient-check-new")
    data = {"ingredients": [ingredient1.name, ingredient2.name, "new ingredient"]}

    response = api_client.post(url, data, format="json")
    assert len(response.data["ingredients"]) == 1

    data.pop("ingredients")
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
