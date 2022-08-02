from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, TemplateView
from mainapp.models import SiteSettings, Review

from adminapp.forms import CourseEditForm, TeacherEditForm, SubjectEditForm, SiteSettingsEditForm, ReviewEditForm
from mainapp.models import Course, Teacher, Subject


class AdminMainView(TemplateView):
    template_name = 'adminapp/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect("/")


# Абстрактные классы
class AdminCreateView(CreateView):
    model = None
    template_name = "adminapp/add-object.html"
    form_class = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
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
            if request.user.is_superuser or request.user.is_staff:
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
            if request.user.is_superuser or request.user.is_staff:
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

    def post(self, request, *args, **kwargs):
        if "test-email" in self.request.POST:
            e_mail = self.request.POST["test-email"]
            send_mail(
                subject=f'Тестовое сообщение от {SiteSettings.objects.all()[0].admin_email}',
                message='Если вы получили данное сообщение - проверка отправки тестового письма выполнена успешно',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[e_mail]
            )
            return HttpResponseRedirect(request.environ['HTTP_REFERER'])
        else:
            return super().post(self, request, *args, **kwargs)

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

    def get_queryset(self):
        return Teacher.objects.order_by('last_name')


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


class ReviewsView(AdminListView):
    model = Review
    template_name = 'adminapp/reviews.html'
    context_object_name = 'reviews'


class ReviewEditView(AdminEditView):
    model = Review
    form_class = ReviewEditForm
    success_url = reverse_lazy("staff:reviews")


class ReviewCreateView(AdminCreateView):
    model = Review
    form_class = ReviewEditForm
    success_url = reverse_lazy("staff:reviews")


class ReviewDeleteView(AdminDeleteView):
    model = Review
    template_name = 'adminapp/confirm-delete-reviews.html'
    success_url = reverse_lazy("staff:reviews")
