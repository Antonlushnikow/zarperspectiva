from django.urls import path
from django.views.generic import TemplateView


from adminapp.views import SiteSettingsEditView, CoursesView, CourseEditView, CourseCreateView, CourseDeleteView, \
    TeachersView, TeacherEditView, TeacherCreateView, TeacherDeleteView


urlpatterns = [
    path('', TemplateView.as_view(template_name='adminapp/index.html'), name='index'),
    path('edit-site/', SiteSettingsEditView.as_view(), name='site-settings'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('edit-course/<int:pk>/', CourseEditView.as_view(), name='edit-course'),
    path('add-course/', CourseCreateView.as_view(), name='add-course'),
    path('delete-course/<int:pk>/', CourseDeleteView.as_view(), name='delete-course'),
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('edit-teacher/<int:pk>/', TeacherEditView.as_view(), name='edit-teacher'),
    path('add-teacher/', TeacherCreateView.as_view(), name='add-teacher'),
    path('delete-teacher/<int:pk>/', TeacherDeleteView.as_view(), name='delete-teacher'),
    ]
