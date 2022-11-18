from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    EMPLOYEE = 'E'
    CLIENT = 'C'
    USER_TYPE_CHOICES = [
        (EMPLOYEE, 'Работник'),
        (CLIENT, 'Клиент'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    tel = models.CharField(max_length=11, verbose_name='Телефон')
    office = models.CharField(
        max_length=200,
        verbose_name='Кабинет',
        blank=True
    )
    position = models.CharField(max_length=200, verbose_name='Должность')
    department = models.CharField(max_length=200, verbose_name='Отдел')
    type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=CLIENT,
        verbose_name='Тип аккаунта'
    )
