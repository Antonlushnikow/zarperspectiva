import hashlib
from random import random

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import SiteUser, Student


class SiteUserLoginForm(AuthenticationForm):
    """
    Форма аутентификации
    """
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите, что вы не робот!"
    )
    username = forms.CharField(label='Логин или электронная почта')

    class Meta:
        model = SiteUser

    def __init__(self, *args, **kwargs):
        super(SiteUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control mb-2"
            field.help_text = ""


class SiteUserRegistrationForm(UserCreationForm):
    """
    Форма регистрации
    """
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите что вы не робот!"
    )
    accept_pdn = forms.BooleanField(required=True, label='\n\r')

    class Meta:
        model = SiteUser
        fields = (
            "username",
            "last_name",
            "first_name",
            "second_name",
            "email",
            "phone",
            "address",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SiteUserRegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != "accept_pdn":
                field.widget.attrs["class"] = "form-control mb-2"
            if field.required:
                field.label_suffix = " (обязательное)"
            field.help_text = ""


class SiteUserUpdateForm(UserChangeForm):
    """
    Форма изменения данных пользователя
    """
    password = None

    class Meta:
        model = SiteUser
        fields = (
            "last_name",
            "first_name",
            "second_name",
            "email",
            "phone",
            "address",
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class SiteUserPasswordChangeForm(PasswordChangeForm):
    """
    Форма смены пароля
    """
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(
        label="Еще раз новый пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = SiteUser
        fields = ("old_password", "new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        super(SiteUserPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class SiteUserConfirmDeleteForm(forms.Form):
    """
    Форма подтверждения удаления пользователя
    """
    password = forms.CharField(
        label="Введите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            "last_name",
            "first_name",
            "second_name",
            "birthday",
            "email",
            "phone",
            "school",
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class SiteUserPasswordResetForm(PasswordResetForm):
    """
    Форма сброса пароля
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class AdminLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите что вы не робот!"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
