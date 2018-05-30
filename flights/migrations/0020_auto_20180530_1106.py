# Generated by Django 2.0.5 on 2018-05-30 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0019_auto_20180530_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='rain',
            field=models.CharField(blank=True, choices=[('NO', 'No recent rain'), ('DURING', 'Rain during spotting'), ('BEFORE', 'Rain before spotting'), ('AFTER', 'Rain after spotting')], max_length=6, null=True),
        ),
    ]
