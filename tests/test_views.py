import pytest
from django.urls import reverse

from claypot.models import Recipe
from claypot.serializers import RecipeSerializer


@pytest.mark.django_db
def test_recipe_detail_view(client, recipe_factory):
    recipe = recipe_factory()
    url = reverse('recipe-detail', kwargs={'pk': recipe.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('factory_type', ['Ingredient', 'Unit'])
@pytest.mark.parametrize(
    'names,search_term,results',
    [
        (['Abc'], 'd', []),
        (['Abc'], 'a', ['Abc']),
        (['Abc', 'aab'], 'a', ['Abc', 'aab']),
        (['Abc', 'aab'], 'c', ['Abc']),
    ]
)
def test_ingredient_list_view(
        client, ingredient_factory, unit_factory, factory_type, names,
        search_term, results):
    if factory_type == 'Ingredient':
        factory = ingredient_factory
        url = reverse('ingredient-list')
    elif factory_type == 'Unit':
        factory = unit_factory
        url = reverse('unit-list')
    else:
        assert False

    for name in names:
        factory(name=name)

    response = client.get(url, {'search': search_term})
    assert response.status_code == 200
    assert set(response.json()['search']) == set(results)


@pytest.mark.django_db
def test_new_recipe(faker, client, unit_factory):
    unit = unit_factory()
    data = {
        "title": faker.name(),
        "instructions": faker.text(),
        "recipe_ingredients": [{
            "ingredient": faker.word(),
            "ingredient_extra": faker.sentence(),
            "optional": False,
            "amount_type": 2,
            "amount_numeric": 1.0,
            "amount_approx": None,
            "unit": str(unit),
        }]
    }
    url = reverse('recipe-create')
    response = client.post(
        url,
        data,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    assert response.status_code == 200, response.content
    recipe_pk = response.json()['id']
    expected = RecipeSerializer(Recipe.objects.get(pk=recipe_pk)).data
    assert response.json() == expected


@pytest.mark.django_db
def test_edit_recipe_add_ingredient(
        faker, client, unit_factory, recipe_factory,
        recipe_ingredient_factory):
    recipe = recipe_factory()
    recipe_ingredient_factory(recipe=recipe)
    unit = unit_factory()
    data = RecipeSerializer(recipe).data
    data['recipe_ingredients'].append({
        "ingredient": faker.word(),
        "ingredient_extra": faker.sentence(),
        "optional": False,
        "amount_type": 2,
        "amount_numeric": 1.0,
        "amount_approx": None,
        "unit": str(unit),
    })
    url = reverse('recipe-update', kwargs={'pk': recipe.pk})
    response = client.post(
        url,
        data,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    assert response.status_code == 200, response.content
    recipe_pk = response.json()['id']
    expected = RecipeSerializer(Recipe.objects.get(pk=recipe_pk)).data
    assert expected['id'] == recipe.pk
    assert len(expected['recipe_ingredients']) == 2
    assert response.json() == expected


@pytest.mark.django_db
def test_edit_recipe_edit_ingredient(
        faker, client, unit_factory, recipe_factory,
        recipe_ingredient_factory):
    recipe = recipe_factory()
    recipe_ingredient_factory(recipe=recipe)
    data = RecipeSerializer(recipe).data
    new_extra_ingredient = faker.sentence()
    data['recipe_ingredients'][0]["ingredient_extra"] = new_extra_ingredient
    url = reverse('recipe-update', kwargs={'pk': recipe.pk})
    response = client.post(
        url,
        data,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    assert response.status_code == 200, response.content
    recipe_pk = response.json()['id']
    expected = RecipeSerializer(Recipe.objects.get(pk=recipe_pk)).data
    assert expected['id'] == recipe.pk
    assert len(expected['recipe_ingredients']) == 1
    assert expected['recipe_ingredients'][0]['ingredient_extra'] == (
        new_extra_ingredient)
    assert response.json() == expected


@pytest.mark.django_db
def test_edit_recipe_remove_ingredient(
        faker, client, unit_factory, recipe_factory,
        recipe_ingredient_factory):
    recipe = recipe_factory()
    recipe_ingredient_factory(recipe=recipe)
    data = RecipeSerializer(recipe).data
    new_extra_ingredient = faker.sentence()
    data['recipe_ingredients'].pop()
    url = reverse('recipe-update', kwargs={'pk': recipe.pk})
    response = client.post(
        url,
        data,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    assert response.status_code == 200, response.content
    recipe_pk = response.json()['id']
    expected = RecipeSerializer(Recipe.objects.get(pk=recipe_pk)).data
    assert expected['id'] == recipe.pk
    assert len(expected['recipe_ingredients']) == 0
    assert response.json() == expected


@pytest.mark.django_db
def test_new_recipe_slug(faker, client, unit_factory):
    unit = unit_factory()
    data = {
        "title": faker.name(),
        "instructions": faker.text(),
        "recipe_ingredients": [{
            "ingredient": faker.word(),
            "ingredient_extra": faker.sentence(),
            "optional": False,
            "amount_type": 2,
            "amount_numeric": 1.0,
            "amount_approx": None,
            "unit": str(unit),
        }]
    }
    url = reverse('recipe-create')
    response = client.post(
        url,
        data,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    assert response.status_code == 200, response.content
    recipe_pk = response.json()['id']
    recipe = Recipe.objects.get(pk=recipe_pk)
    expected = RecipeSerializer(recipe).data
    assert response.json() == expected

    # Add another recipe with the same title
    response = client.post(
        url,
        data,
        content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    recipe_pk2 = response.json()['id']
    recipe2 = Recipe.objects.get(pk=recipe_pk2)

    assert recipe_pk != recipe_pk2
    assert recipe.slug != recipe2.slug


@pytest.mark.django_db
@pytest.mark.parametrize('use_recipe', [True, False])
@pytest.mark.parametrize('use_ajax', [True, False])
def test_get_recipe(client, recipe_factory, use_recipe, use_ajax):
    if use_recipe:
        recipe = recipe_factory()
        url = reverse('recipe-update', kwargs={'pk': recipe.pk})
    else:
        recipe = None
        url = reverse('recipe-create')
    kwargs = {}
    if use_ajax:
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
    response = client.get(url, **kwargs)
    assert response.status_code == 200
    assert (response['Content-Type'] == 'application/json') is use_ajax
    if use_ajax:
        assert response.json() == RecipeSerializer(recipe).data
