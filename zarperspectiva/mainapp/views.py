from django.shortcuts import render
from django.views.generic import ListView
from mainapp.models import Course


class ListCourses(ListView):
    model = Course
