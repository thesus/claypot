import pytest


@pytest.fixture
def factories(
    ingredient_factory,
    unit_factory,
    recipe_factory,
    recipe_ingredient_factory,
    ingredient_tag_factory,
):
    return [
        ingredient_factory,
        unit_factory,
        recipe_factory,
        recipe_ingredient_factory,
        ingredient_tag_factory,
    ]


@pytest.mark.django_db
def test_natural_key(factories):
    for factory in factories:
        obj = factory()
        assert isinstance(str(obj), str)
        cls = obj._meta.model
        natural_key = obj.natural_key()
        from_db = cls.objects.get_by_natural_key(*natural_key)
        assert obj.pk == from_db.pk
