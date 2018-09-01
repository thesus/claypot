from django.conf import settings
import factory
import pytest_factoryboy


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
    title = factory.Faker('words')
    slug = factory.Faker('words')
    instructions = factory.Faker('text')
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = 'claypot.Recipe'
        django_get_or_create = ('slug',)
