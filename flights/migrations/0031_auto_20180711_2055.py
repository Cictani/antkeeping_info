# Generated by Django 2.0.7 on 2018-07-11 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0030_auto_20180711_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='city_long',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='state_long',
            new_name='state',
        ),
    ]
