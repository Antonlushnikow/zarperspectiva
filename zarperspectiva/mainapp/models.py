import datetime

from django.conf import settings
from django.db import models
from tinymce.models import HTMLField

from authapp.models import Student


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
    admin_photo = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='фото администратора',
    )
    admin_email = models.EmailField(
        verbose_name='email администратора',
        null=False,
        default='zarperspectiva@gmail.com'
    )
    admin_phone = models.CharField(
        verbose_name='телефон администратора',
        default='+7-919-367-2831',
        max_length=50,
    )
    address = models.CharField(
        verbose_name='адрес центра',
        default='г. Заречный, ул. Ленинградская, 29А',
        max_length=150,
    )
    vk_link = models.CharField(
        verbose_name='ссылка на ВК',
        default='https://vk.com/public.cpperspektiva',
        max_length=150,
    )
    contacts_info = HTMLField(
        verbose_name='информация о контактах',
        default='На ваши вопросы всегда ответит администратор центра Ольга Валерьевна. Тел. +7-919-367-2831 (с 18 августа по 26 мая по будням с 15.00 до 20.00)',
    )
    center_info = HTMLField(
        verbose_name='информация о центре',
        default='',
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

    info = HTMLField(
        verbose_name='информация',
        null=True,
        default='',
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


class AcademicHour(models.Model):
    duration = models.IntegerField(
        verbose_name='длительность урока',
        null=False,
        default=45,
    )
    price_once = models.CharField(
        verbose_name='разовая оплата (групп)',
        null=False,
        max_length=32,
    )
    price_month = models.CharField(
        verbose_name='абонемент 4 занятия (групп)',
        null=False,
        max_length=32,
    )
    price_once_ind = models.CharField(
        verbose_name='разовая оплата (индивидуально)',
        null=False,
        max_length=32,
        default=750,
    )
    price_month_ind = models.CharField(
        verbose_name='абонемент 4 занятия (индивидуально)',
        null=False,
        max_length=32,
        default=2550,
    )

    def __str__(self):
        return f'{self.duration} минут'

    class Meta:
        verbose_name = 'академический час'
        verbose_name_plural = 'академические часы'
        ordering = ['duration']


class Course(models.Model):
    title = models.CharField(
        verbose_name='название курса',
        max_length=100,
        null=False,
    )
    info = HTMLField(
        verbose_name='информация о курсе',
        blank=True,
        default='',
    )
    subject = models.ManyToManyField(
        Subject,
        verbose_name='предмет',
        related_name='subject',
    )
    age = models.ManyToManyField(
        Age,
        verbose_name='возраст',
        related_name='ages',
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='преподаватель',
        null=True,
        on_delete=models.SET_NULL,
    )
    # price_once_alone = models.IntegerField(
    #     verbose_name='Разовая оплата за занятие (уст.)',
    #     default=600,
    # )
    # price_pass_group = models.IntegerField(
    #     verbose_name='Цена за месяц по абонементу (уст.)',
    #     default=1400,
    # )
    # duration = models.IntegerField(
    #     verbose_name='длительность занятия (уст.)',
    #     default=60,
    # )
    academic_hour = models.ForeignKey(
        AcademicHour,
        verbose_name='длительность занятия',
        related_name='academic_hour',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
        ordering = ['title']


class Pupil(models.Model):
    parent_surname = models.CharField(
        verbose_name='Фамилия заказчика',
        max_length=50,
        null=False,
        blank=False,
    )

    parent_name = models.CharField(
        verbose_name='Имя заказчика',
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

    address_parent = models.CharField(
        verbose_name='адрес',
        max_length=256,
        null=False,
        blank=False,
        default='не указан',
    )

    e_mail_parent = models.EmailField(
        verbose_name='Электронная почта заказчика',
        null=False,
        blank=False,
    )

    surname_pupil = models.CharField(
        verbose_name='Фамилия ученика',
        max_length=50,
        null=False,
        blank=False,
    )

    name_pupil = models.CharField(
        verbose_name='Имя ученика',
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

    student = models.ForeignKey(
        Student,
        verbose_name='ученик',
        related_name='records',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )

    comment = models.TextField(
        verbose_name='комментарий',
        max_length=256,
        null=True,
        blank=True,
        default='',
    )

    def __str__(self):
        return f'{self.surname_pupil} {self.name_pupil} {self.second_name_pupil}'

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'


class Review(models.Model):
    ROLES = [
        ('Родитель', 'Родитель'),
        ('Ученик', 'Ученик'),
    ]

    review_text = HTMLField(
        verbose_name='Текст отзыва',
        default='Введите текст отзыва.',
    )
    author = models.CharField(
        verbose_name='Автор отзыва',
        max_length=300,
        default='Аноним'
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=ROLES,
        default='Родитель'
    )

    def __str__(self):
        return self.review_text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
