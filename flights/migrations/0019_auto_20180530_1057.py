# Generated by Django 2.0.5 on 2018-05-30 08:57

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0018_flight_sky_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='habitat',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
