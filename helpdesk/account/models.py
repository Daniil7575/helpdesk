from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token,
                                 *args, **kwargs):
    print(sender)
    email_plaintext_message = '{}?token={}'.format(
        reverse('account:password_reset:reset-password-confirm'),
        reset_password_token.key
    )

    send_mail(
        'Сброс пароля для HelpDesk',
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )


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

    def __str__(self) -> str:
        return f'Профиль {self.user.username}'
