# Generated by Django 2.2.1 on 2019-06-15 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("images", "0002_image_thumbnail")]

    operations = [
        migrations.AlterModelOptions(name="image", options={"ordering": ["id"]})
    ]
