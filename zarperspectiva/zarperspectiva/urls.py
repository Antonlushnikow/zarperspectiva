from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView


from mainapp.views import SubjectsView, CoursesView, ListCoursesApi, ListSubjectsApi, \
    ListAgesApi, RecordForCourses, export_records


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SubjectsView.as_view(), name='index'),

    path('subject/<slug:slug>/', CoursesView.as_view(), name='subject'),

    path('export/', TemplateView.as_view(template_name='mainapp/export.html'), name='export'),
    path('export-records/', export_records, name='export-records'),


    path('record-for-courses/', RecordForCourses.as_view(), name='record'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('api/courses/', ListCoursesApi.as_view(), name='courses-api'),
    path('api/subjects/', ListSubjectsApi.as_view(), name='subjects-api'),
    path('api/ages/', ListAgesApi.as_view(), name='ages-api'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
