from django import forms

from mainapp.models import Pupil, Subject


class CreateRecordForm(forms.ModelForm):
    """
    Форма создания записи на курс
    """
    subject_choices = [(subj.pk, subj.title) for subj in Subject.objects.all()]
    subjects = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Предметы',
        choices=subject_choices,
    )

    class Meta:
        model = Pupil
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CreateRecordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'subjects':
                field.widget.attrs["class"] = ""
            else:
                field.widget.attrs["class"] = "form-control"
            field.help_text = ""
