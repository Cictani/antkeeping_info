# Generated by Django 2.0.5 on 2018-05-15 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0006_auto_20180515_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='antspecies',
            name='hibernation',
            field=models.CharField(blank=True, choices=[('NO', 'No'), ('LONG', 'yes, around 6 months'), ('SHORT', 'yes, around 3 months')], max_length=5, null=True, verbose_name='Hibernation'),
        ),
    ]
