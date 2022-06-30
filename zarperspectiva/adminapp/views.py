from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from mainapp.models import SiteSettings

from adminapp.forms import SiteSettingsEditForm, CourseEditForm, TeacherEditForm
from mainapp.models import Course, Teacher


class SiteSettingsEditView(UpdateView):
    model = SiteSettings
    template_name = "adminapp/edit-site.html"
    form_class = SiteSettingsEditForm
    success_url = reverse_lazy("staff:site-settings")

    def get_object(self):
        return SiteSettings.objects.all()[0]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(SiteSettingsEditView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class CoursesView(ListView):
    model = Course
    template_name = 'adminapp/courses.html'
    context_object_name = 'courses'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(CoursesView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class CourseEditView(UpdateView):
    model = Course
    template_name = "adminapp/edit-course.html"
    form_class = CourseEditForm
    success_url = reverse_lazy("staff:courses")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(CourseEditView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class CourseCreateView(CreateView):
    model = Course
    template_name = "adminapp/add-course.html"
    form_class = CourseEditForm
    success_url = reverse_lazy("staff:courses")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(CourseCreateView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'adminapp/confirm-delete-course.html'
    success_url = reverse_lazy("staff:courses")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(CourseDeleteView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class TeachersView(ListView):
    model = Teacher
    template_name = 'adminapp/teachers.html'
    context_object_name = 'teachers'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(TeachersView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class TeacherEditView(UpdateView):
    model = Teacher
    template_name = "adminapp/edit-teacher.html"
    form_class = TeacherEditForm
    success_url = reverse_lazy("staff:teachers")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(TeacherEditView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class TeacherCreateView(CreateView):
    model = Teacher
    template_name = "adminapp/add-teacher.html"
    form_class = TeacherEditForm
    success_url = reverse_lazy("staff:teachers")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(TeacherCreateView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'adminapp/confirm-delete-teacher.html'
    success_url = reverse_lazy("staff:teachers")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(TeacherDeleteView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")
