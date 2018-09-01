from django.conf import settings
from django.db import migrations
from django.utils.translation import ugettext_lazy


units = [
    (ugettext_lazy('kilogram'), ugettext_lazy('kilograms'), 'kg'),
    (ugettext_lazy('gram'), ugettext_lazy('grams'), 'g'),
    (ugettext_lazy('litre'), ugettext_lazy('litres'), 'l'),
    (ugettext_lazy('millilitre'), ugettext_lazy('millilitres'), 'ml'),
    (ugettext_lazy('Pinch'), ugettext_lazy('pinches'), ''),

    # Translators: German unit of volume. Cannot really be translate.
    (ugettext_lazy('Teelöffel'), ugettext_lazy('Teelöffel'), 'TL'),
    # Translators: German unit of volume. Cannot really be translate.
    (ugettext_lazy('Esslöffel'), ugettext_lazy('Esslöffel'), 'EL'),
]


def create_units(apps, schema_editor):
    Unit = apps.get_model('claypot', 'Unit')
    for singular, plural, code in units:
        Unit.objects.get_or_create(
            code=code,
            defaults={
                'name': singular,
                'name_plural': plural,
            })


def remove_units(apps, schema_editor):
    Unit = apps.get_model('claypot', 'Unit')
    for _, _, code in units:
        Unit.objects.get(code=code).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('claypot', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_units, remove_units),
    ]
