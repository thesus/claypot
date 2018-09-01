import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_recipe_detail_view(client, recipe_factory):
    recipe = recipe_factory()
    url = reverse('recipe-detail', kwargs={'pk': recipe.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'ingredients,search_term,results',
    [
        (['Abc'], 'd', []),
        (['Abc'], 'a', ['Abc']),
        (['Abc', 'aab'], 'a', ['Abc', 'aab']),
        (['Abc', 'aab'], 'c', ['Abc']),
    ]
)
def test_ingredient_list_view(
        client, ingredient_factory, ingredients, search_term, results):
    for name in ingredients:
        ingredient_factory(name=name)
    url = reverse('ingredient-list')

    response = client.get(url, {'search': search_term})
    assert response.status_code == 200
    assert set(response.json()['search']) == set(results)
