# Generated by Django 4.2.7 on 2024-04-13 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Место проведения', 'verbose_name_plural': 'Места проведения'},
        ),
        migrations.CreateModel(
            name='EventList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_app.category', verbose_name='Категория')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_app.event', verbose_name='Мероприятие')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_app.location', verbose_name='Место проведения')),
            ],
        ),
    ]
