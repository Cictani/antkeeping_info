# Generated by Django 2.0.5 on 2018-05-21 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ants', '0009_auto_20180521_2130'),
        ('flights', '0003_flight_reviewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='ant_regions',
        ),
        migrations.AddField(
            model_name='flight',
            name='city',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='flight',
            name='country',
            field=models.ForeignKey(default=174, on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='ants.AntRegion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flight',
            name='county',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='flight',
            name='state',
            field=models.CharField(default='blub', max_length=150),
            preserve_default=False,
        ),
    ]