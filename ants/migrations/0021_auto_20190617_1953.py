# Generated by Django 2.2.2 on 2019-06-17 17:53

import django.contrib.postgres.fields.ranges
import django.contrib.postgres.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0020_auto_20190617_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='antspecies',
            name='founding',
            field=models.CharField(blank=True, choices=[('c', 'claustral (queen does not need any food)'), ('sc', 'semi-claustral (queen needs to be fed during founding)'), ('sp', 'social parasitic (queen needs workers of suitable ant species)'), ('spp', 'social parasitic (founding can be done with pupae of suitable ant species)')], max_length=3, null=True, verbose_name='Founding'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='hibernation',
            field=models.CharField(blank=True, choices=[('NO', 'No'), ('LONG', 'yes: end of september until end of march'), ('SHORT', 'yes: end of november until end of february')], max_length=5, null=True, verbose_name='Hibernation required'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='nest_humidity',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(100)], verbose_name='Nest relative humidity (%)'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='nest_temperature',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(41)], verbose_name='Nest temperature (℃)'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='outworld_humidity',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(100)], verbose_name='Outworld relative humidty (%)'),
        ),
        migrations.AlterField(
            model_name='antspecies',
            name='outworld_temperature',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='Note that the upper value is not included so if you want to enter 25 - 28 you have to enter 25 - 29', null=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(41)], verbose_name='Outworld temperature (℃)'),
        ),
    ]
