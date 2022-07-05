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
    )
    activation_key = models.CharField(max_length=128, blank=True, verbose_name="ключ активации")
    activation_key_expires = models.DateTimeField(
        default=default_key_expires,
        verbose_name="срок действия ключа активации"
    )

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires
