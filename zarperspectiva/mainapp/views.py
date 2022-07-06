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
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class ListSubjectsApi(APIView):
    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class ListAgesApi(APIView):
    def get(self, request, format=None):
        ages = Age.objects.all()
        serializer = AgeSerializer(ages, many=True)
        return Response(serializer.data)


class RecordForCourses(CreateView):
    model = Pupil
    template_name = "mainapp/record_for_course.html"
    form_class = CreateRecordForm
    success_url = "/"

    def form_valid(self, form):
        if SiteSettings.objects.exists():
            obj = SiteSettings.objects.all()[0]
            admin_email = obj.admin_email
        else:
            admin_email = 'zarpespectiva@gmail.com'

        super_form = super().form_valid(form)
        courses = form.cleaned_data['courses']
        courses_ = [f'{course}' for course in courses]
        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject='Новая запись на курсы',
            message=f'{form.instance.name_pupil} {form.instance.surname_pupil} записался(ась) '
                    f'на курсы: {", ".join(courses_)}\n\n'
                    f'Заявитель: {form.instance.parent_surname} {form.instance.parent_name} '
                    f'{form.instance.parent_second_name}\n'
                    f'Телефон: {form.instance.phone_pupil}',
            recipient_list=[admin_email]
        )

        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject='Поздравляем с успешной записью на курсы',
            message=f'Вы записаны на курсы: {", ".join(courses_)}',
            recipient_list=[form.instance.e_mail_parent],
        )
        return super_form


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
