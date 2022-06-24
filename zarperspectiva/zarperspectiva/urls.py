from django.contrib import admin
from django.urls import path

from mainapp.views import ListCourses, send

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ListCourses.as_view(), name="index"),
    path("send_mail", send, name='send'),

]
