from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    pass


class SiteUser(AbstractUser):
    second_name = models.CharField(
        max_length=30,
        blank=True,
    )
    students = models.ManyToManyField(
        Student,
        verbose_name='ученики',
        related_name='parent',
    )
