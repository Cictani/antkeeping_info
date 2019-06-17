# Generated by Django 2.2.2 on 2019-06-17 13:36

from  antkeeping_info.db_fields import IntegerRangeField
import django.contrib.postgres.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0019_auto_20190617_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antspecies',
            name='nest_humidity',
            field=IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(100)], verbose_name='Nest relative humidity (%)'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='nest_temperature',
            field=IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(41)], verbose_name='Nest temperature (℃)'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='outworld_humidity',
            field=IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(100)], verbose_name='Outworld relative humidty (%)'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='outworld_temperature',
            field=IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(41)], verbose_name='Outworld temperature (℃)'),
        ),
    ]
