from mainapp.models import SiteSettings


def get_site_settings(request):
    if SiteSettings.objects.exists():
        obj = SiteSettings.objects.all()[0]
        return {
            "site_info": obj.site_info,
            "letter_template": obj.letter_template,
            "schedule_url": obj.schedule_url,
            "calendar_url": obj.calendar_url,
        }
    return {}
