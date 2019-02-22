from django.urls import reverse
from rest_framework import status
import pytest

from claypot.api import serializers


@pytest.mark.django_db
def test_tagging(
        recipe_factory, recipe_ingredient_factory, ingredient_tag_factory):
    recipe = recipe_factory()
    assert recipe.tags() == set()
    recipe_ingredient = recipe_ingredient_factory(recipe=recipe)
    tag1 = ingredient_tag_factory()
    recipe_ingredient.ingredient.tags.add(tag1)
    assert recipe.tags() == set((tag1,))


@pytest.mark.django_db
def test_recipe_list(api_client, recipe_factory, user):
    recipe = recipe_factory(author=user)
    api_client.force_login(user)
    recipe_details = api_client.get(reverse('api:recipe-detail', kwargs={'pk': recipe.pk}))
    assert recipe_details.data['is_starred'] is False
    recipe_star = api_client.post(reverse('api:recipe-star', kwargs={'pk': recipe.pk}))
    assert recipe_star.data is True
    recipe_details = api_client.get(reverse('api:recipe-detail', kwargs={'pk': recipe.pk}))
    assert recipe_details.data['is_starred'] is True
    recipe_unstar = api_client.post(reverse('api:recipe-unstar', kwargs={'pk': recipe.pk}))
    assert recipe_unstar.data is False
    recipe_details = api_client.get(reverse('api:recipe-detail', kwargs={'pk': recipe.pk}))
    assert recipe_details.data['is_starred'] is False


@pytest.mark.django_db
def test_post_new_recipe(
        api_client, recipe, recipe_ingredient_factory,
        recipe_ingredient_group_factory,
        recipe_ingredient_group_ingredient_factory, user):
    recipe_ingredient_factory(recipe=recipe, order=1)
    group = recipe_ingredient_group_factory(recipe=recipe, order=2)
    recipe_ingredient_group_ingredient_factory(group=group, order=1)
    api_client.force_login(user)
    url = reverse('api:recipe-detail', kwargs={'pk': recipe.pk})
    src = serializers.RecipeSerializer(instance=recipe).data
    data = {
      "title": src['title'],
      "instructions": src['instructions'],
      "ingredients": [i for i in src['ingredients'] if i['is_group'] is not True],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert [i for i in response.data['ingredients'] if i['is_group'] is True] == []
    assert len([i for i in response.data['ingredients'] if i['is_group'] is False]) > 0
