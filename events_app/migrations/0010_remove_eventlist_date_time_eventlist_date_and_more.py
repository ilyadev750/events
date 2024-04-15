# Generated by Django 4.2.7 on 2024-04-15 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0009_alter_location_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlist',
            name='date_time',
        ),
        migrations.AddField(
            model_name='eventlist',
            name='date',
            field=models.DateField(default=datetime.date(2024, 4, 20), verbose_name='Дата мероприятия'),
        ),
        migrations.AddField(
            model_name='eventlist',
            name='time',
            field=models.TimeField(default=datetime.time(10, 0), verbose_name='Время мероприятия'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=200, verbose_name='Название мероприятия'),
        ),
    ]