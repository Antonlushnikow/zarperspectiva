from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from mainapp.views import SubjectsView, CoursesView, ListCoursesApi, ListSubjectsApi, ListAgesApi, send

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SubjectsView.as_view(), name='index'),

    path('courses/', CoursesView.as_view(), name='courses'),
    path('api/courses/', ListCoursesApi.as_view(), name='courses-api'),
    path('api/subjects/', ListSubjectsApi.as_view(), name='subjects-api'),
    path('api/ages/', ListAgesApi.as_view(), name='ages-api'),

    path("send_mail", send, name='send'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
