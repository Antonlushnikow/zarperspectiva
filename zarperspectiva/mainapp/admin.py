from django.contrib import admin

from .models import SiteSettings, Subject, Teacher

admin.site.register(SiteSettings)
admin.site.register(Subject)
admin.site.register(Teacher)
