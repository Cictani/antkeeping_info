# Generated by Django 2.2 on 2019-04-28 14:02

import ants.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0014_auto_20190428_1558'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='genus',
            managers=[
                ('objects', ants.managers.GenusManager()),
            ],
        ),
    ]
