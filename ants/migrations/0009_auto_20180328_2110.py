# Generated by Django 2.0.3 on 2018-03-28 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0008_auto_20180326_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distribution',
            name='protected',
            field=models.NullBooleanField(verbose_name='Protected by law'),
        ),
    ]