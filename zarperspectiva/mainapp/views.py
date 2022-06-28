from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, CreateView

from mainapp.forms import CreateRecordForm
from mainapp.models import Subject, Course, Pupil

from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.models import Subject, Course, Age
from zarperspectiva import settings

from mainapp.serializers import CourseSerializer, SubjectSerializer, AgeSerializer
import csv


MODELS = {
    'pupil': (
        Pupil,
        [
            'name_pupil',
            'surname_pupil',
            'second_name_pupil',
            'birthday_pupil',
            'phone_pupil'
        ]
    ),
    'course': (
        Course,
        [
            'title',
        ]
    )
}


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


def export_model(model_name: str):
    model, headers = MODELS[model_name]
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    writer = csv.writer(response)
    writer.writerow(headers)
    objects = model.objects.all().values_list()
    for obj in objects:
        writer.writerow(obj)
    return response


def export_students(request):
    return export_model('pupil')


def export_courses(request):
    return export_model('course')


def export_records(request):
    model = Course
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    writer = csv.writer(response)
    objects = model.objects.select_related('subject')
    print(objects.query)
    objects = objects.values_list()
    print(objects.values_list())
    for obj in objects:
        writer.writerow(obj)
    return response
