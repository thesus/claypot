# Generated by Django 2.1.5 on 2019-05-04 14:24

from django.db import migrations
import uuid


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return

    Recipe = apps.get_model("claypot", "Recipe")
    for recipe in Recipe.objects.all():
        recipe.slug = str(uuid.uuid4())
        recipe.save()


class Migration(migrations.Migration):

    dependencies = [("claypot", "0004_recipe_parent_recipe")]

    operations = [migrations.RunPython(forwards)]
