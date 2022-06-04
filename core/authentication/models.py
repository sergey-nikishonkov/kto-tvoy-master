from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    """Model provides custom authentication whit phone number as a username"""

    phone = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(regex=r'^((\+7|7|8)+([0-9]){10})$',
                           message='Введите корректный номер телефона'),
        ],
        unique=True,
        verbose_name='Номер телефонa')
    role = models.CharField(max_length=255, null=True, blank=True, verbose_name='Роль')
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
