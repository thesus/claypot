# Generated by Django 3.0 on 2019-12-25 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("claypot", "0013_auto_20191005_1952"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredientgroup",
            name="title",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterUniqueTogether(
            name="recipeingredientgroup",
            unique_together={("recipe", "order", "title")},
        ),
    ]