from datetime import (
    datetime,
    timedelta,
)

from django.urls import reverse
from pytz import utc
from rest_framework import status
import pytest

from claypot.api import serializers

from claypot.models import (
    Recipe
)

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
      "images": [],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert [i for i in response.data['ingredients'] if i['is_group'] is True] == []
    assert len([i for i in response.data['ingredients'] if i['is_group'] is False]) > 0


@pytest.mark.django_db
def test_fork_recipe(
        api_client, recipe_factory,
        recipe_ingredient_factory,
        recipe_ingredient_group_ingredient_factory,
        recipe_ingredient_group_factory,
        user):

    orig = recipe_factory()
    recipe_ingredient_factory(recipe=orig)

    group = recipe_ingredient_group_factory(recipe=orig, order=2)
    recipe_ingredient_group_ingredient_factory(group=group, order=1)

    api_client.force_login(user)

    url = reverse('api:recipe-fork', kwargs={'pk': orig.pk})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    fork = Recipe.objects.get(pk=response.data)

    assert orig.pk == fork.parent_recipe.pk
    assert orig.instructions.count() == fork.instructions.count()
    # Check sporadically if the groups are correctly copied.
    orig_ingredient = orig.ingredient_groups.first().ingredients.first()
    fork_ingredient = fork.ingredient_groups.first().ingredients.first()
    assert orig_ingredient.ingredient == fork_ingredient.ingredient
    assert orig_ingredient.amount_type == fork_ingredient.amount_type


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_settings,published_recently,should_work',
    [
        [{}, True, True],
        [{}, False, False],
        [{'is_superuser': True}, True, True],
        [{'is_superuser': True}, False, True],
        [{'is_staff': True}, True, True],
        [{'is_staff': True}, False, True],
    ],
)
def test_remove_recipe(
        api_client, recipe, user, user_settings, published_recently, settings,
        should_work):
    for attr, value in user_settings.items():
        setattr(user, attr, value)
    if len(user_settings) > 0:
        user.save()

    now = datetime.utcnow().replace(tzinfo=utc)
    recipe.published_on = now - timedelta(seconds=1)
    if not published_recently:
        recipe.published_on -= settings.RECIPE_DELETE_GRACE_PERIOD
    recipe.save()

    api_client.force_login(user)

    url = reverse('api:recipe-detail', kwargs={'pk': recipe.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['deletable'] == should_work

    response = api_client.delete(url)
    if should_work:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
