from django.urls import path


from adminapp.views import SiteSettingsEditView, CoursesView, CourseEditView, CourseCreateView, CourseDeleteView, \
    TeachersView, TeacherEditView, TeacherCreateView, TeacherDeleteView, SubjectDeleteView, SubjectCreateView, \
    SubjectsView, SubjectEditView, AdminMainView, ReviewsView, ReviewEditView, ReviewCreateView, ReviewDeleteView

urlpatterns = [
    path('', AdminMainView.as_view(), name='index'),
    path('edit-site/', SiteSettingsEditView.as_view(), name='site-settings'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('edit-course/<int:pk>/', CourseEditView.as_view(), name='edit-course'),
    path('add-course/', CourseCreateView.as_view(), name='add-course'),
    path('delete-course/<int:pk>/', CourseDeleteView.as_view(), name='delete-course'),
    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('edit-teacher/<int:pk>/', TeacherEditView.as_view(), name='edit-teacher'),
    path('add-teacher/', TeacherCreateView.as_view(), name='add-teacher'),
    path('delete-teacher/<int:pk>/', TeacherDeleteView.as_view(), name='delete-teacher'),
    path('subjects/', SubjectsView.as_view(), name='subjects'),
    path('edit-subject/<int:pk>/', SubjectEditView.as_view(), name='edit-subject'),
    path('add-subject/', SubjectCreateView.as_view(), name='add-subject'),
    path('delete-subject/<int:pk>/', SubjectDeleteView.as_view(), name='delete-subject'),
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path('edit-review/<int:pk>/', ReviewEditView.as_view(), name='edit-review'),
    path('add-review/', ReviewCreateView.as_view(), name='add-review'),
    path('delete-review/<int:pk>/', ReviewDeleteView.as_view(), name='delete-review'),
    ]
