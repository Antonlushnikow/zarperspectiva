from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from mainapp.views import SubjectsView, CoursesView, ListCoursesApi, ListSubjectsApi, \
    ListAgesApi, RecordForCourses, export_records, ScheduleView

from mainapp.utils import export_courses_to_xls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SubjectsView.as_view(), name='index'),

    path('subject/<slug:slug>/', CoursesView.as_view(), name='subject'),

    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('contacts/', TemplateView.as_view(template_name='mainapp/contacts.html'), name='contacts'),
    path('export/', TemplateView.as_view(template_name='mainapp/export.html'), name='export'),
    path('export-records/', export_records, name='export-records'),
    path('export-courses/', export_courses_to_xls, name='export-courses'),


    path('record-for-courses/', RecordForCourses.as_view(), name='record'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('api/courses/', ListCoursesApi.as_view(), name='courses-api'),
    path('api/subjects/', ListSubjectsApi.as_view(), name='subjects-api'),
    path('api/ages/', ListAgesApi.as_view(), name='ages-api'),

    path("staff/", include(("adminapp.urls", "adminapp"), namespace="staff")),
    path("auth/", include(("authapp.urls", "authapp"), namespace="auth")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
