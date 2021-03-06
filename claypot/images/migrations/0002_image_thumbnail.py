# Generated by Django 2.2.1 on 2019-06-05 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("images", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="image",
            name="thumbnail",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="parent",
                to="images.ImageFile",
            ),
        )
    ]
