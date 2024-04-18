from django.db import models
from django.contrib.auth.models import User
from events_app.models import EventList


class Token(models.Model):
    """Модель JWT токена"""

    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
        )
    access_token = models.CharField(
        max_length=400, verbose_name='access_token'
        )
    refresh_token = models.CharField(
        max_length=400, verbose_name='refresh_token'
        )

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"
        unique_together = ()

    def __str__(self) -> str:
        return f'{self.user_id}'


class EventRegistration(models.Model):
    """Модель регистрации на мероприятие"""
    event_list_id = models.ForeignKey(
        EventList, on_delete=models.CASCADE, verbose_name="Событие"
        )
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
        )
    is_registered = models.BooleanField(
        default=True, verbose_name="Зарегистрирован"
        )

    class Meta:
        verbose_name = "Регистрация на мероприятие"
        verbose_name_plural = "Регистрации на мероприятия"
        unique_together = ('event_list_id', 'user_id', 'is_registered')

    def __str__(self) -> str:
        return f'{self.event_list_id} - {self.user_id}'
