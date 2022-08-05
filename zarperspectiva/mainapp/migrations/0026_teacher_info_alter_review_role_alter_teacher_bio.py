# Generated by Django 4.0.5 on 2022-08-04 15:46

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0025_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='info',
            field=tinymce.models.HTMLField(default='', null=True, verbose_name='информация'),
        ),
        migrations.AlterField(
            model_name='review',
            name='role',
            field=models.CharField(choices=[('Родитель', 'Родитель'), ('Ученик', 'Ученик')], default='Родитель', max_length=20, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='bio',
            field=models.TextField(null=True, verbose_name='о себе (на удаление)'),
        ),
    ]