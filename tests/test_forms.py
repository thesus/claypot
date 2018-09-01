from django.urls import reverse
import pytest

from claypot.forms import RecipeIngredientCreateForm
from claypot.models import (
    AMOUNT_TYPE_APPROX,
    AMOUNT_TYPE_NONE,
    AMOUNT_TYPE_NUMERIC,
)


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


@pytest.mark.django_db
@pytest.mark.parametrize('amount_numeric', [False, True])
@pytest.mark.parametrize('amount_approx', [False, True])
@pytest.mark.parametrize('unit', [False, True])
def test_recipe_ingredient_form_amount_type_none(
        recipe_factory, ingredient_factory, unit_factory, amount_numeric,
        amount_approx, unit):
    recipe = recipe_factory()
    ingredient = ingredient_factory()
    data = dict(RecipeIngredientCreateForm().initial)
    data['recipe'] = recipe.pk
    data['ingredient'] = ingredient.pk
    data['amount_type'] = AMOUNT_TYPE_NONE
    expected_errors = set()

    if amount_numeric:
        data['amount_numeric'] = 1.0
        expected_errors.add('numeric-amount-given')
    else:
        data['amount_numeric'] = ''
    if amount_approx:
        data['amount_approx'] = 'some'
        expected_errors.add('approximated-amount-given')
    else:
        data['amount_approx'] = ''
    if unit:
        data['unit'] = unit_factory().pk
        expected_errors.add('unit-given')
    else:
        data['unit'] = ''

    form = RecipeIngredientCreateForm(data=data)
    assert form.is_valid() is (len(expected_errors) == 0)
    existing_errors = set()
    for field_errors in form.errors.as_data().values():
        for field_error in field_errors:
            existing_errors.add(field_error.code)
    assert existing_errors == set(expected_errors), form.errors.as_data()


@pytest.mark.django_db
@pytest.mark.parametrize('amount_numeric', [False, True])
@pytest.mark.parametrize('amount_approx', [False, True])
@pytest.mark.parametrize('unit', [False, True])
def test_recipe_ingredient_form_amount_type_numeric(
        recipe_factory, ingredient_factory, unit_factory, amount_numeric,
        amount_approx, unit):
    recipe = recipe_factory()
    ingredient = ingredient_factory()
    data = dict(RecipeIngredientCreateForm().initial)
    data['recipe'] = recipe.pk
    data['ingredient'] = ingredient.pk
    data['amount_type'] = AMOUNT_TYPE_NUMERIC
    expected_errors = set()

    if amount_numeric:
        data['amount_numeric'] = 1.0
    else:
        data['amount_numeric'] = ''
        expected_errors.add('numeric-amount-missing')
    if amount_approx:
        data['amount_approx'] = 'some'
        expected_errors.add('approximated-amount-given')
    else:
        data['amount_approx'] = ''
    if unit:
        data['unit'] = unit_factory().pk
    else:
        data['unit'] = ''
        expected_errors.add('unit-missing')

    form = RecipeIngredientCreateForm(data=data)
    assert form.is_valid() is (len(expected_errors) == 0)
    existing_errors = set()
    for field_errors in form.errors.as_data().values():
        for field_error in field_errors:
            existing_errors.add(field_error.code)
    assert existing_errors == set(expected_errors), form.errors.as_data()


@pytest.mark.django_db
@pytest.mark.parametrize('amount_numeric', [False, True])
@pytest.mark.parametrize('amount_approx', [False, True])
@pytest.mark.parametrize('unit', [False, True])
def test_recipe_ingredient_form_amount_type_approx(
        recipe_factory, ingredient_factory, unit_factory, amount_numeric,
        amount_approx, unit):
    recipe = recipe_factory()
    ingredient = ingredient_factory()
    data = dict(RecipeIngredientCreateForm().initial)
    data['recipe'] = recipe.pk
    data['ingredient'] = ingredient.pk
    data['amount_type'] = AMOUNT_TYPE_APPROX
    expected_errors = set()

    if amount_numeric:
        data['amount_numeric'] = 1.0
        expected_errors.add('numeric-amount-given')
    else:
        data['amount_numeric'] = ''
    if amount_approx:
        data['amount_approx'] = 'some'
    else:
        data['amount_approx'] = ''
        expected_errors.add('approximated-amount-missing')
    if unit:
        data['unit'] = unit_factory().pk
        expected_errors.add('unit-given')
    else:
        data['unit'] = ''

    form = RecipeIngredientCreateForm(data=data)
    assert form.is_valid() is (len(expected_errors) == 0)
    existing_errors = set()
    for field_errors in form.errors.as_data().values():
        for field_error in field_errors:
            existing_errors.add(field_error.code)
    assert existing_errors == set(expected_errors), form.errors.as_data()
