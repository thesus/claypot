# Generated by Django 2.2.5 on 2019-10-05 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claypot', '0012_recipedraft'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipedraft',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='recipedraft',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drafts', to='claypot.Recipe'),
        ),
    ]
