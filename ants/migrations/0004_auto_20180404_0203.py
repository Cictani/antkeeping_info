# Generated by Django 2.0.4 on 2018-04-04 00:03

import ants.models
from decimal import Decimal
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0003_auto_20180404_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antsize',
            name='maximum',
            field=ants.models.SizeField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Maximum (mm)'),
        ),
        migrations.AlterField(
            model_name='antsize',
            name='minimum',
            field=ants.models.SizeField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Minimum (mm)'),
        ),
    ]
