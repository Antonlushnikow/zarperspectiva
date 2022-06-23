from django.contrib import admin

from .models import SiteSettings, Subject, Teacher, Age, Course

admin.site.register(SiteSettings)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Age)
admin.site.register(Course)
