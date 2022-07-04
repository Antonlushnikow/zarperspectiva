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

from .models import SiteUser


class SiteUserLoginForm(AuthenticationForm):
    """
    Форма аутентификации
    """
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите, что вы не робот!"
    )

    class Meta:
        model = SiteUser
        fields = ("username", "password")

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

    class Meta:
        model = SiteUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SiteUserRegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control mb-2"
            if field.required:
                field.label_suffix = " (обязательное)"
            field.help_text = ""

    def save(self, commit=True):
        user = super(SiteUserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode("utf8")).hexdigest()[:6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode("utf8")
        ).hexdigest()
        user.save()
        return user


class SiteUserUpdateForm(UserChangeForm):
    """
    Форма изменения данных пользователя
    """
    password = None
    avatar = forms.FileField(label="Аватар", widget=forms.FileInput())

    class Meta:
        model = SiteUser
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(SiteUserUpdateForm, self).__init__(*args, **kwargs)
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


class SiteUserPasswordResetForm(PasswordResetForm):
    """
    Форма сброса пароля
    """
    def __init__(self, *args, **kwargs):
        super(SiteUserPasswordResetForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
            