# Generated by Django 2.0.6 on 2018-06-02 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='official_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
