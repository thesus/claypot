import pytest


@pytest.mark.django_db
def test_tagging(
        recipe_factory, recipe_ingredient_factory, ingredient_tag_factory):
    recipe = recipe_factory()
    assert recipe.tags() == set()
    recipe_ingredient = recipe_ingredient_factory(recipe=recipe)
    tag1 = ingredient_tag_factory()
    recipe_ingredient.ingredient.tags.add(tag1)
    assert recipe.tags() == set((tag1,))
