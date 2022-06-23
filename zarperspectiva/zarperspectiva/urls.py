from django.contrib import admin
from django.urls import path

from mainapp.views import CoursesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CoursesView.as_view()),
]
