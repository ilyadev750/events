from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    access_token = models.CharField(max_length=200, verbose_name='access_token')
    refresh_token = models.CharField(max_length=200, verbose_name='refresh_token')

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"

    def __str__(self) -> str:
        return f'{self.user_id}'
