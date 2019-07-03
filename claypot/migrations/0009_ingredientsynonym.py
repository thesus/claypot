# Generated by Django 2.2.2 on 2019-07-03 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claypot', '0008_auto_20190528_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientSynonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synonyms', to='claypot.Ingredient')),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
    ]
