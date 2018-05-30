# Generated by Django 2.0.5 on 2018-05-30 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0017_auto_20180530_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='sky_condition',
            field=models.CharField(blank=True, choices=[('CLEAR', 'Clear / Sunny'), ('MCLEAR', 'Mostly Clear / Mostly Sunny'), ('PCLOUDY', 'Partly Cloudy / Partly Sunny'), ('MCLOUDY', 'Mostly Cloudy / Considerable Cloudiness'), ('CLOUDY', 'Cloudy'), ('FAIR', 'Fair')], max_length=7, null=True),
        ),
    ]
