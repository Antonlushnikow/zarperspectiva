# Generated by Django 4.0.5 on 2022-06-24 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_age_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='subjects/', verbose_name='фон предмета'),
        ),
    ]