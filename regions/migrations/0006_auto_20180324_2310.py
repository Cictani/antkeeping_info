# Generated by Django 2.0.3 on 2018-03-24 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0005_auto_20180324_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='ant_list_complete',
        ),
        migrations.RemoveField(
            model_name='region',
            name='ant_list_complete',
        ),
    ]
