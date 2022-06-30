from mainapp.models import SiteSettings
from django import forms


class SiteSettingsEditForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SiteSettingsEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
