from django.db import models
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    site_info = HTMLField(
        verbose_name='информация о сайте',
        default='Информация',
    )
    letter_template = HTMLField(
        verbose_name='шаблон письма',
        default='Спасибо за заявку',
    )


class Subject(models.Model):
    title = models.CharField(
        verbose_name='название',
        null=False,
        max_length=40,
    )


class Teacher(models.Model):
    first_name = models.CharField(
        verbose_name='имя',
        max_length=30,
        null=False,
    )
    parent_name = models.CharField(
        verbose_name='отчество',
        max_length=30,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=40,
        null=False,
    )
    pic = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='фото',
    )
    bio = models.TextField(
        verbose_name='о себе',
        null=True,
    )

    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.parent_name}'
