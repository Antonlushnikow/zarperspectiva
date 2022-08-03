from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta
from django.utils.timezone import now


def default_key_expires():
    return now() + timedelta(hours=24)


class SiteUser(AbstractUser):
    first_name = models.CharField(
        verbose_name="имя",
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=150,
        blank=False,
    )
    second_name = models.CharField(
        max_length=30,
        blank=False,
        verbose_name='отчество',
    )

    email = models.EmailField(
        verbose_name="электронная почта",
        blank=False,
    )

    phone = models.CharField(
        verbose_name='телефон',
        max_length=12,
        null=False,
        blank=False,
    )

    activation_key = models.CharField(max_length=128, blank=True, verbose_name="ключ активации")
    activation_key_expires = models.DateTimeField(
        default=default_key_expires,
        verbose_name="срок действия ключа активации",
    )

    is_verified = models.BooleanField(
        verbose_name='почта подтверждена',
        default=False,
    )

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def is_activation_key_too_young(self, minutes):
        return (self.activation_key_expires - now()) > timedelta(hours=23, minutes=(60-minutes))

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Student(models.Model):
    first_name = models.CharField(
        verbose_name="имя",
        max_length=150,
        blank=False,
    )
    second_name = models.CharField(
        verbose_name="отчество",
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        verbose_name="электронная почта",
        blank=True
    )
    parent = models.ForeignKey(
        SiteUser,
        verbose_name='родитель',
        related_name='students',
        on_delete=models.CASCADE,
        default=None,
    )
    phone = models.CharField(
        verbose_name="телефон",
        max_length=20,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name='дата рождения',
        default=datetime(2010, 1, 1),
        null=False,
    )
    school = models.CharField(
        verbose_name='Место учебы',
        default='не указано',
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = 'ученик'
        verbose_name_plural = 'ученики'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.second_name}'
