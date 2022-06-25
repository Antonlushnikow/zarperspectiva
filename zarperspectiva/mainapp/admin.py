from django.contrib import admin

from .models import SiteSettings, Subject, Teacher, Age, Course


class SubjectAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(SiteSettings)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher)
admin.site.register(Age)
admin.site.register(Course)
