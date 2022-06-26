from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from mainapp.views import SubjectsView, CoursesView, CourseDetailView, send, RecordForCourses

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SubjectsView.as_view(), name='index'),

    path('subject/<slug:slug>/', CoursesView.as_view(), name='subject'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course'),
    path('record-for-courses/', RecordForCourses.as_view(), name='record'),

    path("send_mail", send, name='send'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
