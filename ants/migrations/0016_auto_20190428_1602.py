# Generated by Django 2.2 on 2019-04-28 14:02

from django.db import migrations

from ants.migration_operations import add_generic_species_for_each_genus


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0015_auto_20190428_1602'),
    ]

    operations = [
        migrations.RunPython(add_generic_species_for_each_genus)
    ]
