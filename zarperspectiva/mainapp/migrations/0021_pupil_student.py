# Generated by Django 4.0.5 on 2022-07-28 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_alter_student_options_remove_siteuser_students_and_more'),
        ('mainapp', '0020_academichour_alter_course_info_course_academic_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupil',
            name='student',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='authapp.student', verbose_name='ученик'),
        ),
    ]
