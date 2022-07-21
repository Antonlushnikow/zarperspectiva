import csv

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.forms import CreateRecordForm
from mainapp.models import Subject, Course, Age, Pupil, SiteSettings, Teacher
from zarperspectiva import settings
from mainapp.serializers import CourseSerializer, SubjectSerializer, AgeSerializer


class SubjectsView(ListView):
    model = Subject
    template_name = 'mainapp/index.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.order_by('?')[:4]
        return context

    def get_queryset(self):
        return Subject.objects.order_by('title')


class CoursesView(ListView):
    model = Course
    template_name = 'mainapp/courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.order_by('age')


class ListCoursesApi(APIView):
    def get(self, request, format=None):
        age_id = request.query_params.get("ageId")
        subject_id = request.query_params.get("subjId")
        if age_id and subject_id:
            data = Course.objects.filter(age__id=age_id, subject__id=subject_id).order_by('age')
        elif age_id and not subject_id:
            data = Course.objects.filter(age__id=age_id).order_by('age')
        elif not age_id and subject_id:
            data = Course.objects.filter(subject__id=subject_id).order_by('age')
        else:
            data = Course.objects.all()
        serializer = CourseSerializer(data, many=True)

        return Response(serializer.data)


class ListSubjectsApi(APIView):
    """
    Класс возвращает список всех предметов, если в запросе нет параметров.
    Если в запросе есть параметр ageId, то возвращаются только предметы, подходящие по возрасту.
    """

    def get(self, request, format=None):
        data = []
        id = request.query_params.get("ageId")
        if id is not None and id != '':
            courses = Course.objects.filter(age__id=id).all()
            for course in courses:
                for subject in course.subject.all():
                    data.append(subject)
        else:
            data = Subject.objects.all()
        serializer = SubjectSerializer(set(data), many=True)
        return Response(serializer.data)


class ListAgesApi(APIView):
    """
    Возвращает только возраста, для которых имеются активные курсы.
    """

    def get(self, request, format=None):
        courses = Course.objects.prefetch_related('age').all()
        data = []
        for course in courses:
            for age in course.age.all():
                data.append(age)
        serializer = AgeSerializer(set(data), many=True)
        return Response(serializer.data)


class RecordForCourses(CreateView):
    model = Pupil
    template_name = "mainapp/record_for_course.html"
    form_class = CreateRecordForm
    success_url = "/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if SiteSettings.objects.exists():
            obj = SiteSettings.objects.all()[0]
            admin_email = obj.admin_email
        else:
            admin_email = 'zarpespectiva@gmail.com'

    def process_templates(self, template: str, obj):
        template = template.replace('$client_name', " ".join(
            [obj.parent_name, obj.parent_second_name, obj.parent_name]))
        template = template.replace('$pupil_name', " ".join(
            [obj.name_pupil, obj.surname_pupil, obj.second_name_pupil]))
        template = template.replace('$phone_parent', obj.phone_parent)
        template = template.replace('$e_mail_parent', obj.e_mail_parent)
        template = template.replace('$birthday_pupil', str(obj.birthday_pupil))
        template = template.replace('$school_pupil', obj.school_pupil)
        if obj.phone_pupil:
            template = template.replace('$phone_pupil', obj.phone_pupil)
        if obj.e_mail_pupil:
            template = template.replace('$e_mail_pupil', obj.e_mail_pupil)
        template = template.replace('$sign_up_date', str(obj.sign_up_date))

        template = template.replace('$courses', "<br>".join([course.title for course in obj.courses.all()]))
        return template

    def form_valid(self, form):
        obj = form.save()
        admin_message_text = SiteSettings.objects.get().admin_letter_template
        client_message_text = SiteSettings.objects.get().client_letter_template
        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject='Новая запись на курсы',
            message=self.process_templates(admin_message_text, obj),
            recipient_list=[SiteSettings.objects.get().admin_email],
            html_message=self.process_templates(admin_message_text, obj),
        )

        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject='Поздравляем с успешной записью на курсы',
            message=self.process_templates(client_message_text, obj),
            recipient_list=[obj.e_mail_parent],
            html_message=self.process_templates(client_message_text, obj),
        )
        return HttpResponseRedirect("/")


@login_required
def export_records(request):
    model = Pupil
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')

    writer.writerow([
        'Фамилия ученика',
        'Имя ученика',
        'Отчество ученика',
        'Телефон ученика',
        'Email ученика',
        'День рождения',
        'Место учебы',
        'Класс',
        'Фамилия заказчика',
        'Имя заказчика',
        'Отчество заказчика',
        'Телефон заказчика',
        'Email заказчика',
        'Серия, номер паспорта',
        'Дата выдачи',
        'Орган выдачи',
        'Город проживания',
        'Улица, дом проживания',
        'Дата заявки',
        'Предметы',
    ])

    for obj in model.objects.values_list(
            'surname_pupil',
            'name_pupil',
            'second_name_pupil',
            'phone_pupil',
            'e_mail_pupil',
            'birthday_pupil',
            'school_pupil',
            'courses__age',
            'parent_surname',
            'parent_name',
            'parent_second_name',
            'phone_parent',
            'e_mail_parent',
            'sign_up_date',
            'courses__title',
    ):
        obj_ = obj[:13] + ('', '', '', '', '') + obj[13:]
        writer.writerow(obj_)
    return response


class ScheduleView(DetailView):
    model = SiteSettings
    template_name = "mainapp/schedule.html"
    context_object_name = "content"

    def get_object(self, queryset=None):
        if SiteSettings.objects.exists():
            obj = SiteSettings.objects.all()[0]
        else:
            obj = SiteSettings.objects.create()
            obj.save()
        return obj


class TeachersListView(ListView):
    model = Teacher
    template_name = 'mainapp/teachers.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return Teacher.objects.order_by('last_name')


class TeacherView(DetailView):
    model = Teacher
    template_name = 'mainapp/teacher.html'
    context_object_name = 'teacher'
