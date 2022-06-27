from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.models import Subject, Course
from zarperspectiva import settings

from mainapp.serializers import CourseSerializer


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


class CourseDetailView(DetailView):
    model = Course
    template_name = 'mainapp/course.html'
    context_object_name = 'course'


def send(request):
    send_to = "ashiryaev84@gmail.com"
    title = f"Тема для тестового письма"
    message = f"Тело письма. Привет это письмо от зарперспективы"
    send_mail(
        title, message, settings.EMAIL_HOST_USER, [send_to], fail_silently=False
    )
    return HttpResponseRedirect("/")
