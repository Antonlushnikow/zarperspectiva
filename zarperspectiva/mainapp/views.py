import csv

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.forms import CreateRecordForm
from mainapp.models import Subject, Course, Age, Pupil, SiteSettings
from zarperspectiva import settings
from mainapp.serializers import CourseSerializer, SubjectSerializer, AgeSerializer


class SubjectsView(ListView):
    model = Subject
    template_name = 'mainapp/index.html'
    context_object_name = 'subjects'


class CoursesView(ListView):
    model = Course
    template_name = 'mainapp/courses.html'
    context_object_name = 'courses'


class ListCoursesApi(APIView):
    def get(self, request, format=None):
        age_id = request.query_params.get("ageId")
        subject_id = request.query_params.get("subjId")
        data = Course.objects.filter(age__id=age_id, subject__id=subject_id).all()
        serializer = CourseSerializer(data, many=True)
        return Response(serializer.data)


class ListSubjectsApi(APIView):
    """
    Класс возвращает список всех предметов, если в запросе нет параметров.
    Если в запросе есть параметр ageId, то возвращаются только предметы, подходящие по возрасту.
    """

    def get(self, request, format=None):
        id = request.query_params["ageId"]
        if id is not None and id != '':
            courses = Course.objects.filter(age__id=id).all()
            data = (course.subject for course in courses)
        else:
            data = Subject.objects.all()
        serializer = SubjectSerializer(data, many=True)
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
        serializer = AgeSerializer(data, many=True)
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
        'Фамилия родителя',
        'Имя родителя',
        'Отчество родителя',
        'Email родителя',
        'Фамилия ученика',
        'Имя ученика',
        'Отчество ученика',
        'День рождения',
        'Предмет',
    ])

    for obj in model.objects.values_list(
            'parent_surname',
            'parent_name',
            'parent_second_name',
            'e_mail_parent',
            'surname_pupil',
            'name_pupil',
            'second_name_pupil',
            'birthday_pupil',
            'courses__title',
    ):
        writer.writerow(obj)
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
