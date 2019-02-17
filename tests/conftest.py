from django.conf import settings
import factory
import pytest
import pytest_factoryboy


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest_factoryboy.register
class UserFactory(factory.DjangoModelFactory):
    username = factory.Faker('name')

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)


@pytest_factoryboy.register
class IngredientFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = 'claypot.Ingredient'
        django_get_or_create = ('name',)


@pytest_factoryboy.register
class UnitFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')
    name_plural = factory.Faker('name')
    code = factory.Faker('word')

    class Meta:
        model = 'claypot.Unit'
        django_get_or_create = ('name',)


@pytest_factoryboy.register
class RecipeFactory(factory.DjangoModelFactory):
    title = factory.Faker('sentence')
    slug = factory.Faker('sentence')
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = 'claypot.Recipe'
        django_get_or_create = ('slug',)


@pytest_factoryboy.register
class RecipeIngredientFactory(factory.DjangoModelFactory):
    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    order = factory.Faker('random_int')
    ingredient_extra = factory.Faker('word')
    optional = factory.Faker('boolean')
    amount_numeric = factory.Faker('random_number')
    unit = factory.SubFactory(UnitFactory)

    class Meta:
        model = 'claypot.RecipeIngredient'
        django_get_or_create = ('recipe', 'ingredient')


@pytest_factoryboy.register
class IngredientTagFactory(factory.DjangoModelFactory):
    tag = factory.Faker('word')

    class Meta:
        model = 'claypot.IngredientTag'
        django_get_or_create = ('tag',)
