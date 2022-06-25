from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from mainapp.models import Subject, Course
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from zarperspectiva import settings


class SubjectsView(ListView):
    model = Subject
    template_name = 'mainapp/index.html'
    context_object_name = 'subjects'


class CoursesView(ListView):
    model = Course
    template_name = 'mainapp/courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        subject = get_object_or_404(Subject, slug=self.kwargs["slug"])
        return Course.objects.filter(subject__in=[subject])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["subject"] = get_object_or_404(Subject, slug=self.kwargs["slug"])
        return context


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
