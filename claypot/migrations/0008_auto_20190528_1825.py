# Generated by Django 2.2.1 on 2019-05-28 18:25

from django.db import migrations

from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension


class Migration(migrations.Migration):

    dependencies = [("claypot", "0007_auto_20190524_1834")]

    operations = [TrigramExtension(), UnaccentExtension()]