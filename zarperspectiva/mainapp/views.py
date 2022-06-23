from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from zarperspectiva import settings
from django.views.generic import ListView
from mainapp.models import Course


class ListCourses(ListView):
    model = Course
    template_name = "mainapp/index.html"


def send(request):
    send_to = "ashiryaev84@gmail.com"
    title = f"Тема для тестового письма"
    message = f"Тело письма. Привет это письмо от зарперспективы"
    send_mail(
        title, message, settings.EMAIL_HOST_USER, [send_to], fail_silently=False
    )
    return HttpResponseRedirect("/")