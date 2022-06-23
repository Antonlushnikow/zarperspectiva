from django.shortcuts import render
from django.views.generic import ListView
from mainapp.models import Course


class CoursesView(ListView):
    model = Course
    template_name = 'mainapp/index.html'
    context_object_name = 'courses'
