from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms

from mainapp.models import Pupil, Subject


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateRecordForm(forms.ModelForm):
    """
    Форма создания записи на курс
    """
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите что вы не робот!"
    )

    class Meta:
        model = Pupil
        fields = "__all__"
        widgets = {
            'birthday_pupil': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CreateRecordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'subjects':
                field.widget.attrs["class"] = ""
            else:
                field.widget.attrs["class"] = "form-control"
            field.help_text = ""
