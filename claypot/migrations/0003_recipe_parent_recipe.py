# Generated by Django 2.1.5 on 2019-04-28 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claypot', '0002_auto_20190428_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='parent_recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='claypot.Recipe'),
        ),
    ]
