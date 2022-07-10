from django.contrib import admin

from .models import SiteUser, Student

admin.site.register(SiteUser)
admin.site.register(Student)
