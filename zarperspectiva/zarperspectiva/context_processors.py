from django.urls import reverse_lazy

from mainapp.models import SiteSettings


def get_menu_items(request):
    return {
        'main_menu': {
            'КОНТАКТЫ': reverse_lazy('contacts'),
            'ИНФОРМАЦИЯ': reverse_lazy('schedule'),
            'КУРСЫ': reverse_lazy('courses'),
            'УЧИТЕЛЯ': reverse_lazy('teachers'),
            'ЗАПИСЬ': reverse_lazy('record'),
        }
    }


def get_site_settings(request):
    if SiteSettings.objects.exists():
        obj = SiteSettings.objects.all()[0]
        return {
            "site_info": obj.site_info,
            "admin_letter_template": obj.admin_letter_template,
            "client_letter_template": obj.client_letter_template,
            "schedule_url": obj.schedule_url,
            "calendar_url": obj.calendar_url,
        }
    return {}
