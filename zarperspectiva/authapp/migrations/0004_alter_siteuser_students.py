# Generated by Django 4.0.5 on 2022-07-06 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_alter_siteuser_options_siteuser_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='parent', to='authapp.student', verbose_name='ученики'),
        ),
    ]
