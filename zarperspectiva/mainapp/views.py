from django.shortcuts import render
from django.views.generic import ListView
from mainapp.models import Subject


class CoursesView(ListView):
    model = Subject
    template_name = 'mainapp/index.html'
    context_object_name = 'subjects'
