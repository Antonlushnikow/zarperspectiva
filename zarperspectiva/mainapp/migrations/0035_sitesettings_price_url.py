# Generated by Django 4.0.5 on 2024-07-31 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0034_sitesettings_address_sitesettings_admin_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='price_url',
            field=models.CharField(default='', max_length=150, verbose_name='ссылка на прайс'),
        ),
    ]
