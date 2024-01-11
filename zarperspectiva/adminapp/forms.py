from mainapp.models import SiteSettings, Course, Teacher, Subject, Review, AcademicHour
from django import forms


class AdminEditForm(forms.ModelForm):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class SiteSettingsEditForm(AdminEditForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class CourseEditForm(AdminEditForm):
    class Meta:
        model = Course
        fields = '__all__'


class TeacherEditForm(AdminEditForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class SubjectEditForm(AdminEditForm):
    class Meta:
        model = Subject
        fields = '__all__'


class ReviewEditForm(AdminEditForm):
    class Meta:
        model = Review
        fields = '__all__'


class PriceEditForm(AdminEditForm):
    class Meta:
        model = AcademicHour
        fields = '__all__'
