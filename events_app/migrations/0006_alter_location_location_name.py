# Generated by Django 4.2.7 on 2024-04-14 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0005_alter_location_city_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_name',
            field=models.CharField(max_length=400, verbose_name='Название места'),
        ),
    ]
