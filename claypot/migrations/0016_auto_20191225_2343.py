# Generated by Django 3.0 on 2019-12-25 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("claypot", "0015_auto_20191225_2241"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipeingredientgroupingredient",
            options={
                "verbose_name": "Recipe ingredient",
                "verbose_name_plural": "Recipe ingredients",
            },
        ),
        migrations.DeleteModel(name="RecipeIngredient",),
    ]
