import datetime

from django.conf import settings
from django.db import models
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    site_info = HTMLField(
        verbose_name='информация о сайте',
        default='Информация',
    )
    admin_letter_template = HTMLField(
        verbose_name='шаблон письма администратору',
        default='Поступила новая заявка',
    )
    client_letter_template = HTMLField(
        verbose_name='шаблон письма клиенту',
        default='Спасибо за заявку',
    )
    schedule_url = models.CharField(
        verbose_name='ссылка на расписание',
        default='',
        max_length=150,
    )
    calendar_url = models.CharField(
        verbose_name='ссылка на календарь',
        default='',
        max_length=150,
    )

    admin_email = models.EmailField(
        verbose_name='email администратора',
        null=False,
        default='zarperspectiva@gmail.com'
    )

    terms_conditions = models.TextField(
        verbose_name='Политика конфиденциальности и обработки персональных данных',
        default=''
    )

    class Meta:
        verbose_name = 'Настройки сайта'


class Subject(models.Model):
    title = models.CharField(
        verbose_name='название',
        null=False,
        max_length=40,
    )
    pic = models.ImageField(
        upload_to='subjects/',
        null=True,
        blank=True,
        verbose_name='фон предмета',
    )
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Teacher(models.Model):
    first_name = models.CharField(
        verbose_name='имя',
        max_length=30,
        null=False,
    )
    second_name = models.CharField(
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
        return f'{self.last_name} {self.first_name} {self.second_name}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Age(models.Model):
    age = models.CharField(
        verbose_name='возраст',
        null=False,
        max_length=30,
    )

    def __str__(self):
        return self.age

    class Meta:
        verbose_name = 'Возрастная категория'
        verbose_name_plural = 'Возрастные категории'


class Course(models.Model):
    title = models.CharField(
        verbose_name='название курса',
        max_length=100,
        null=False,
    )
    info = models.TextField(
        verbose_name='информация о курсе',
        blank=True,
        default=f'''Индивидуальные занятия возможны только при наличии возможности у педагога и при отсутствии групп. Про возможность индивидуальных занятий уточняйте у администратора центра ({settings.DOMAIN_NAME + "/contacts/"})
                Стоимость индивидуальных занятий
                45 минут – 2550 руб. абонемент 4 занятия/разовая оплата -750 руб.
                60 минут - 3400 руб. абонемент 4 занятия/разовая оплата -1000 руб.
                90 минут - 5100 руб. абонемент 4 занятия/разовая оплата -1500 руб.'''
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name='предмет',
        null=True,
        on_delete=models.SET_NULL,
        related_name='subject',
    )
    age = models.ManyToManyField(
        Age,
        verbose_name='возраст',
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='преподаватель',
        null=True,
        on_delete=models.SET_NULL,
    )
    price_once_alone = models.IntegerField(
        verbose_name='Разовая оплата за занятие',
        default=600,
    )
    price_pass_group = models.IntegerField(
        verbose_name='Цена за месяц по абонементу',
        default=1400,
    )
    duration = models.IntegerField(
        verbose_name='длительность занятия',
        default=60,
    )
    count_a_week = models.IntegerField(
        verbose_name='занятий в неделю',
        default=1,
    )
    count_overall = models.IntegerField(
        verbose_name='занятий всего',
        default=10,
    )
    group_size = models.CharField(
        verbose_name='размер группы',
        blank=True,
        max_length=30,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Pupil(models.Model):
    parent_name = models.CharField(
        verbose_name='Имя заказчика',
        max_length=50,
        null=False,
        blank=False,
    )

    parent_surname = models.CharField(
        verbose_name='Фамилия заказчика',
        max_length=50,
        null=False,
        blank=False,
    )

    parent_second_name = models.CharField(
        verbose_name='Отчество заказчика',
        max_length=50,
        null=False,
        blank=False,
    )

    phone_parent = models.CharField(
        verbose_name='Телефон заказчика',
        max_length=12,
        null=False,
        blank=False,
    )

    e_mail_parent = models.EmailField(
        verbose_name='Электронная почта заказчика',
        null=False,
        blank=False,
    )

    name_pupil = models.CharField(
        verbose_name='Имя ученика',
        max_length=50,
        null=False,
        blank=False,
    )

    surname_pupil = models.CharField(
        verbose_name='Фамилия ученика',
        max_length=50,
        null=False,
        blank=False,
    )

    second_name_pupil = models.CharField(
        verbose_name='Отчество ученика',
        max_length=50,
    )

    birthday_pupil = models.DateField(
        verbose_name='дата рождения ученика',
        null=False,
    )

    school_pupil = models.CharField(
        verbose_name='Место учебы',
        max_length=100,
    )

    phone_pupil = models.CharField(
        verbose_name='Телефон ученика',
        max_length=12,
        null=True,
        blank=True,
    )

    e_mail_pupil = models.EmailField(
        verbose_name='Электронная почта ученика',
        null=True,
        blank=True,
    )

    courses = models.ManyToManyField(Course)

    sign_up_date = models.DateField(
        verbose_name='дата записи',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.surname_pupil} {self.name_pupil} {self.second_name_pupil}'

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
