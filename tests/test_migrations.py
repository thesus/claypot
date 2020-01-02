from django.apps import apps
from django.test import TestCase
from django.db.migrations.executor import MigrationExecutor
from django.db import connection


class MigrationTestCase(TestCase):
    """Migrates database to a specified version and tests migration."""

    migrate_from = None
    migrate_to = None
    app_name = None

    def setUp(self):
        """Django test case setup."""

        # Include app name in migrations
        migrate_from = ((self.app_name, self.migrate_from),)
        migrate_to = ((self.app_name, self.migrate_to),)

        executor = MigrationExecutor(connection)

        # Get old app state
        old_apps = executor.loader.project_state(migrate_from).apps

        executor.migrate(migrate_from)

        self.setup_before_migration(old_apps)

        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(migrate_to)

        # Store the app state on the instance, since the tests are called independently
        self.apps = executor.loader.project_state(migrate_to).apps

    def setup_before_migration(self, apps):
        """Runs before the migration to test is migrated.

        This has to be implemented in test class.
        """
        pass


class RecipeIngredientTestCase(MigrationTestCase):
    migrate_from = "0014_auto_20191225_2240"
    migrate_to = "0015_auto_20191225_2241"
    app_name = "claypot"

    recipe = None

    def setup_before_migration(self, apps):
        Recipe = apps.get_model("claypot", "Recipe")
        RecipeIngredient = apps.get_model("claypot", "RecipeIngredient")
        Ingredient = apps.get_model("claypot", "Ingredient")

        recipe = Recipe.objects.create(title="recipe")
        self.recipe = recipe.id

        RecipeIngredient.objects.create(
            ingredient=Ingredient.objects.create(name="ingredient"),
            recipe=recipe,
            order=0,
        )

    def test_ingredient(self):
        Recipe = self.apps.get_model("claypot", "Recipe")
        recipe = Recipe.objects.get(pk=self.recipe)
        assert recipe.ingredients.count() == 1
