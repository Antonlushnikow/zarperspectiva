from django.db import models
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    site_info = HTMLField(
        verbose_name='информация о сайте',
        default='Информация',
    )
    letter_template = HTMLField(
        verbose_name='шаблон письма',
        default='Спасибо за заявку',
    )


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


class Teacher(models.Model):
    first_name = models.CharField(
        verbose_name='имя',
        max_length=30,
        null=False,
    )
    parent_name = models.CharField(
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
        return f'{self.last_name} {self.first_name} {self.parent_name}'


class Age(models.Model):
    age = models.CharField(
        verbose_name='возраст',
        null=False,
        max_length=30,
    )

    def __str__(self):
        return self.age


class Course(models.Model):
    title = models.CharField(
        verbose_name='название курса',
        max_length=100,
        null=False,
    )
    info = models.TextField(
        verbose_name='информация о курсе',
        blank=True,
    )
    subject = models.ManyToManyField(
        Subject,
        verbose_name='предмет',
    )
    age = models.ManyToManyField(
        Age,
        verbose_name='возраст',
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='преподаватель',
        on_delete=models.DO_NOTHING,
    )
    price_once_alone = models.IntegerField(
        verbose_name='цена за занятие без группы',
        default=600,
    )
    price_pass_alone = models.IntegerField(
        verbose_name='цена за месяц без группы',
        default=1600,
    )
    price_once_group = models.IntegerField(
        verbose_name='цена за занятие без группы',
        default=500,
    )
    price_pass_group = models.IntegerField(
        verbose_name='цена за месяц без группы',
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

    phone_pupil = models.IntegerField(
        verbose_name='Телефоно ученика',
        null=False,
        blank=False,
    )

    e_mail_pupil = models.EmailField(
        verbose_name='Электронная почта',
        null=False,
        blank=False,
    )

    name_pupil = models.CharField(
        verbose_name='Имя ученика',
        max_length=50,
        null=False,
    )

    surname_pupil = models.CharField(
        verbose_name='Фамилия ученика',
        max_length=50,
        null=False,
    )

    second_name_pupil = models.CharField(
        verbose_name='Отчество ученика',
        max_length=50,
    )

    birthday_pupil = models.DateField(
        verbose_name='дата рождения ученика',
        null=False,
    )

    school = models.CharField(
        verbose_name='Место учебы',
        max_length=50,
    )

    phone_parent = models.IntegerField(
        verbose_name='Телефоно заказчика',
        null=True,
    )

    e_mail_parent = models.EmailField(
        verbose_name='Электронная почта заказчика',
        null=True,
    )

    courses = models.ManyToManyField(Course)

    def __str__(self):
        return " ".join([self.name_pupil, self.second_name_pupil, self.surname_pupil])
