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
class RecipeFactory(factory.DjangoModelFactory):
    title = factory.Faker('words')
    slug = factory.Faker('words')
    instructions = factory.Faker('text')
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = 'claypot.Recipe'
        django_get_or_create = ('slug',)
