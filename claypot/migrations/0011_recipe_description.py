# Generated by Django 2.2.2 on 2019-07-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("claypot", "0010_auto_20190709_1847")]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="description",
            field=models.TextField(blank=True, verbose_name="Additional information"),
        )
    ]