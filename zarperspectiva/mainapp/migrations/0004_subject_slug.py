# Generated by Django 4.0.5 on 2022-06-24 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_subject_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(default='fizika', max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
