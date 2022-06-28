from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, CreateView

from mainapp.forms import CreateRecordForm
from mainapp.models import Subject, Course, Pupil

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.models import Subject, Course, Age
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
        super_form = super().form_valid(form)
        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject='Новый ученик успешно записался',
            message=f'Здравствуйте,\n {form.instance.name_pupil} {form.instance.surname_pupil} записался' +
                    f'курсы : ',
            recipient_list=[settings.ADMIN_EMAIL_ADDRESS]
        )

        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject='Поздравляем с успешной записью на курсы',
            message=f'Здравствуйте, ваш ребенок\n {form.instance.name_pupil} {form.instance.surname_pupil} ' +
                    f' записан на курсы : ',
            recipient_list=[form.instance.e_mail_parent],
        )
        return super_form
