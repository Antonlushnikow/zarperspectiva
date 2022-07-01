# Generated by Django 4.0.5 on 2022-06-30 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_sitesettings_calendar_url_sitesettings_schedule_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='calendar_url',
            field=models.CharField(default='', max_length=150, verbose_name='ссылка на календарь'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='schedule_url',
            field=models.CharField(default='', max_length=150, verbose_name='ссылка на расписание'),
        ),
    ]