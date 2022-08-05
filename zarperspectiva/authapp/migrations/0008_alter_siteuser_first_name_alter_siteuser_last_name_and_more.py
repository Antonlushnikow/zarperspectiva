# Generated by Django 4.0.5 on 2022-07-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_alter_siteuser_email_alter_siteuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='second_name',
            field=models.CharField(max_length=30, verbose_name='отчество'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.CharField(blank=True, default='не указано', max_length=100, verbose_name='Место учебы'),
        ),
        migrations.AlterField(
            model_name='student',
            name='second_name',
            field=models.CharField(max_length=150, verbose_name='отчество'),
        ),
    ]
