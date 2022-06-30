from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView
from mainapp.models import SiteSettings

from adminapp.forms import SiteSettingsEditForm


class SiteSettingsEditView(UpdateView):
    model = SiteSettings
    template_name = "adminapp/edit-site.html"
    form_class = SiteSettingsEditForm
    success_url = reverse_lazy("staff:site-settings")

    def get_object(self):
        return SiteSettings.objects.all()[0]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super(SiteSettingsEditView, self).dispatch(
                    request, *args, **kwargs
                )
        return HttpResponseRedirect("/")
