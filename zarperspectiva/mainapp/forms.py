from django import forms

from mainapp.models import Pupil


class CreateRecordForm(forms.ModelForm):
    """
    Форма создания записи на курс
    """
    class Meta:
        model = Pupil
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CreateRecordForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
