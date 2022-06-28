import csv

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.forms import CreateRecordForm
from mainapp.models import Subject, Course, Age, Pupil
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


def send(request):
    send_to = "ashiryaev84@gmail.com"
    title = f"Тема для тестового письма"
    message = f"Тело письма. Привет это письмо от зарперспективы"
    send_mail(
        title, message, settings.EMAIL_HOST_USER, [send_to], fail_silently=False
    )
    return HttpResponseRedirect("/")


class RecordForCourses(CreateView):
    model = Pupil
    template_name = "mainapp/record_for_course.html"
    form_class = CreateRecordForm
    success_url = "/"


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
            'subjects__title',
    ):
        writer.writerow(obj)
    return response
