from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from mainapp.models import SiteSettings

from adminapp.forms import CourseEditForm, TeacherEditForm, SubjectEditForm, SiteSettingsEditForm
from mainapp.models import Course, Teacher, Subject


# Абстрактные классы
class AdminCreateView(CreateView):
    model = None
    template_name = "adminapp/add-object.html"
    form_class = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class AdminEditView(UpdateView):
    model = None
    template_name = "adminapp/edit-object.html"
    form_class = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class AdminListView(ListView):
    model = None
    template_name = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


class AdminDeleteView(DeleteView):
    model = None
    template_name = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")


# CRUD для SiteSettings
class SiteSettingsEditView(AdminEditView):
    model = SiteSettings
    template_name = 'adminapp/edit-sitesettings.html'
    form_class = SiteSettingsEditForm
    success_url = reverse_lazy("staff:site-settings")

    def get_object(self):
        return SiteSettings.objects.all()[0]


# CRUD для Course
class CoursesView(AdminListView):
    model = Course
    template_name = 'adminapp/courses.html'
    context_object_name = 'courses'


class CourseEditView(AdminEditView):
    model = Course
    form_class = CourseEditForm
    success_url = reverse_lazy("staff:courses")


class CourseCreateView(AdminCreateView):
    model = Course
    form_class = CourseEditForm
    success_url = reverse_lazy("staff:courses")


class CourseDeleteView(AdminDeleteView):
    model = Course
    template_name = 'adminapp/confirm-delete-course.html'
    success_url = reverse_lazy("staff:courses")


# CRUD для Teacher
class TeachersView(AdminListView):
    model = Teacher
    template_name = 'adminapp/teachers.html'
    context_object_name = 'teachers'


class TeacherEditView(AdminEditView):
    model = Teacher
    form_class = TeacherEditForm
    success_url = reverse_lazy("staff:teachers")


class TeacherCreateView(AdminCreateView):
    model = Teacher
    form_class = TeacherEditForm
    success_url = reverse_lazy("staff:teachers")


class TeacherDeleteView(AdminDeleteView):
    model = Teacher
    template_name = 'adminapp/confirm-delete-teacher.html'
    success_url = reverse_lazy("staff:teachers")


# CRUD для Teacher
class SubjectsView(AdminListView):
    model = Subject
    template_name = 'adminapp/subjects.html'
    context_object_name = 'subjects'


class SubjectEditView(AdminEditView):
    model = Subject
    form_class = SubjectEditForm
    success_url = reverse_lazy("staff:subjects")


class SubjectCreateView(AdminCreateView):
    model = Subject
    form_class = SubjectEditForm
    success_url = reverse_lazy("staff:subjects")


class SubjectDeleteView(AdminDeleteView):
    model = Subject
    template_name = 'adminapp/confirm-delete-subject.html'
    success_url = reverse_lazy("staff:subjects")