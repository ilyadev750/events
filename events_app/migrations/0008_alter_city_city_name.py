# Generated by Django 4.2.7 on 2024-04-15 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0007_alter_location_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_name',
            field=models.CharField(max_length=100, verbose_name='Город'),
        ),
    ]
