# Generated by Django 4.2.7 on 2024-04-15 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0008_alter_city_city_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('location_name', 'city_id')},
        ),
    ]
