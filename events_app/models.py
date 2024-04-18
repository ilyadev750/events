from django.db import models
import datetime


class Category(models.Model):
    """Модель категории"""
    category_name = models.CharField(
        max_length=100, verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Категория мероприятия"
        verbose_name_plural = "Категории мероприятий"

    def __str__(self):
        return f'{self.category_name}'


class City(models.Model):
    """Модель города"""
    city_name = models.CharField(
        max_length=100, verbose_name="Город"
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f'{self.city_name}'


class Location(models.Model):
    """Модель локации"""
    location_name = models.CharField(
        max_length=400, verbose_name="Название места"
    )
    city_id = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name="Город"
        )

    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"
        unique_together = ('location_name', 'city_id',)

    def __str__(self):
        return f'{self.location_name} - г. {self.city_id}'


class Event(models.Model):
    """Модель события"""
    event_name = models.CharField(
        max_length=200, verbose_name="Название мероприятия"
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f'{self.event_name}'


class EventList(models.Model):
    """Модель списка событий"""
    event_id = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name="Мероприятие"
        )
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
        )
    location_id = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Место проведения"
        )
    date = models.DateField(
        verbose_name="Дата мероприятия", default=datetime.date(2024, 4, 20)
        )
    time = models.TimeField(
        verbose_name="Время мероприятия", default=datetime.time(10, 0, 0)
        )
    price = models.IntegerField(verbose_name="Цена билета", default=0)

    class Meta:
        verbose_name = "Список мероприятий"
        verbose_name_plural = "Список мероприятий"

    def __str__(self):
        return (f'{self.event_id} - {self.location_id}'
                f' - {self.date} - {self.time}')
