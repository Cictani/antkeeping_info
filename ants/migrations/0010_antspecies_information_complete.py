# Generated by Django 2.0.5 on 2018-06-01 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0009_auto_20180521_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='antspecies',
            name='information_complete',
            field=models.BooleanField(default=False, verbose_name='Information complete'),
        ),
    ]