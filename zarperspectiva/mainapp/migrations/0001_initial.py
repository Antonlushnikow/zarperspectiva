# Generated by Django 4.0.5 on 2022-06-22 17:52

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_info', tinymce.models.HTMLField(default='Информация', verbose_name='информация о сайте')),
                ('letter_template', tinymce.models.HTMLField(default='Спасибо за заявку', verbose_name='шаблон письма')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='название')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='имя')),
                ('parent_name', models.CharField(max_length=30, verbose_name='отчество')),
                ('last_name', models.CharField(max_length=40, verbose_name='фамилия')),
                ('pic', models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='фото')),
                ('bio', models.TextField(null=True, verbose_name='о себе')),
                ('subjects', models.ManyToManyField(to='mainapp.subject')),
            ],
        ),
    ]
