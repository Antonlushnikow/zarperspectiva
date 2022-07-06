from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta
from django.utils.timezone import now


def default_key_expires():
    return now() + timedelta(hours=24)


class Student(models.Model):
    pass


class SiteUser(AbstractUser):
    second_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='отчество',
    )
    students = models.ManyToManyField(
        Student,
        verbose_name='ученики',
        related_name='parent',
        blank=True,
    )
    activation_key = models.CharField(max_length=128, blank=True, verbose_name="ключ активации")
    activation_key_expires = models.DateTimeField(
        default=default_key_expires,
        verbose_name="срок действия ключа активации"
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
