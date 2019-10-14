import pytest

from datetime import datetime, timedelta
from pytz import utc

from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from claypot.api import serializers

from claypot.models import Recipe, RECIPE_RELATION_TYPE_ADDITION


@pytest.mark.django_db
def test_tagging(recipe_factory, recipe_ingredient_factory, ingredient_tag_factory):
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
    recipe_details = api_client.get(
        reverse("api:recipe-detail", kwargs={"pk": recipe.pk})
    )
    assert recipe_details.data["is_starred"] is False
    recipe_star = api_client.post(reverse("api:recipe-star", kwargs={"pk": recipe.pk}))
    assert recipe_star.data is True
    recipe_details = api_client.get(
        reverse("api:recipe-detail", kwargs={"pk": recipe.pk})
    )
    assert recipe_details.data["is_starred"] is True
    recipe_unstar = api_client.post(
        reverse("api:recipe-unstar", kwargs={"pk": recipe.pk})
    )
    assert recipe_unstar.data is False
    recipe_details = api_client.get(
        reverse("api:recipe-detail", kwargs={"pk": recipe.pk})
    )
    assert recipe_details.data["is_starred"] is False


@pytest.mark.django_db
def test_search_recipe_list(api_client, recipe_factory, user):
    recipe = recipe_factory(author=user)

    response = api_client.get(reverse("api:recipe-list") + f"?search={recipe.title}")
    assert response.data.get("count") == 1


@pytest.mark.django_db
def test_post_new_recipe(
    api_client,
    recipe,
    recipe_ingredient_factory,
    recipe_ingredient_group_factory,
    recipe_ingredient_group_ingredient_factory,
    user,
):
    recipe_ingredient_factory(recipe=recipe, order=1)
    group = recipe_ingredient_group_factory(recipe=recipe, order=2)
    recipe_ingredient_group_ingredient_factory(group=group, order=1)
    api_client.force_login(user)
    url = reverse("api:recipe-detail", kwargs={"pk": recipe.pk})
    src = serializers.RecipeSerializer(instance=recipe).data
    data = {
        "title": src["title"],
        "description": src["description"],
        "instructions": src["instructions"],
        "ingredients": [i for i in src["ingredients"] if i["is_group"] is not True],
        "images": [],
        "estimated_work_duration": None,
        "estimated_waiting_duration": None,
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert [i for i in response.data["ingredients"] if i["is_group"] is True] == []
    assert len([i for i in response.data["ingredients"] if i["is_group"] is False]) > 0


@pytest.mark.django_db
def test_fork_recipe(
    api_client,
    recipe_factory,
    recipe_ingredient_factory,
    recipe_ingredient_group_ingredient_factory,
    recipe_ingredient_group_factory,
    user,
):

    orig = recipe_factory()
    recipe_ingredient_factory(recipe=orig)

    group = recipe_ingredient_group_factory(recipe=orig, order=2)
    recipe_ingredient_group_ingredient_factory(group=group, order=1)

    api_client.force_login(user)

    url = reverse("api:recipe-fork", kwargs={"pk": orig.pk})
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
    "user_settings,published_recently,should_work",
    [
        [{}, True, True],
        [{}, False, False],
        [{"is_superuser": True}, True, True],
        [{"is_superuser": True}, False, True],
        [{"is_staff": True}, True, True],
        [{"is_staff": True}, False, True],
    ],
)
def test_remove_recipe(
    api_client, recipe, user, user_settings, published_recently, settings, should_work
):
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

    url = reverse("api:recipe-detail", kwargs={"pk": recipe.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["deletable"] == should_work

    response = api_client.delete(url)
    if should_work:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_recipe_relations(api_client, recipe_factory, user):
    recipe1 = recipe_factory(author=user)
    recipe2 = recipe_factory(author=user)
    recipe3 = recipe_factory(author=user)
    api_client.force_login(user)

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe1.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe2.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe3.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }

    url = reverse("api:reciperelation-list")
    data = {
        "recipe1": recipe1.pk,
        "recipe2": recipe2.pk,
        "type": RECIPE_RELATION_TYPE_ADDITION,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe1.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1
    assert (
        (response.json()["results"][0]["recipe1"]["id"] == recipe1.pk)
        and (response.json()["results"][0]["recipe2"]["id"] == recipe2.pk)
    ) or (
        (response.json()["results"][0]["recipe1"]["id"] == recipe2.pk)
        and (response.json()["results"][0]["recipe2"]["id"] == recipe1.pk)
    )
    recipe_relation_id = response.json()["results"][0]["id"]

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe2.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1
    assert (
        (response.json()["results"][0]["recipe1"]["id"] == recipe1.pk)
        and (response.json()["results"][0]["recipe2"]["id"] == recipe2.pk)
    ) or (
        (response.json()["results"][0]["recipe1"]["id"] == recipe2.pk)
        and (response.json()["results"][0]["recipe2"]["id"] == recipe1.pk)
    )

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe3.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }

    url = reverse("api:reciperelation-detail", kwargs={"pk": recipe_relation_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe1.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe2.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }

    url = reverse("api:reciperelation-list")
    response = api_client.get(url, {"recipe": recipe3.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


@pytest.mark.django_db
def test_recipe_drafts(api_client, recipe_factory, user):
    """Tests creating a recipe drafts with and without a recipe."""

    recipe = recipe_factory()

    data = {"data": {"title": "test"}, "recipe": recipe.pk}

    api_client.force_login(user)
    response = api_client.post(reverse("api:recipedraft-list"), data, format="json")

    # Check if draft is associated with recipe and user
    assert response.status_code == 201
    recipe.refresh_from_db()
    assert recipe.drafts.first().author == user

    response = api_client.get(reverse("api:recipedraft-list"))
    assert response.status_code == 200

    # Created draft belongs to a recipe and is not shown in the listing
    assert response.data.get("count") == 0

    # Get detail view of newly created draft
    response = api_client.get(
        reverse("api:recipedraft-detail", kwargs={"pk": recipe.drafts.first().pk})
    )
    assert response.status_code == 200

    # Create draft without an associated recipe -> should be in the list
    data["recipe"] = ""

    response = api_client.post(reverse("api:recipedraft-list"), data, format="json")
    assert response.status_code == 201

    response = api_client.get(reverse("api:recipedraft-list"))
    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert response.data.get("results")[0].get("title") == "test"
