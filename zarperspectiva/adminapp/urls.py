from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from adminapp.views import SiteSettingsEditView


urlpatterns = [
    path('edit-site/', SiteSettingsEditView.as_view(), name='site-settings'),
    ]
