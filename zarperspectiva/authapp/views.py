# from allauth.account.signals import user_signed_up
import hashlib
from random import random

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    SiteUserRegistrationForm,
    SiteUserLoginForm,
)
from .models import SiteUser, default_key_expires


def send_verify_mail(user):
    salt = hashlib.sha1(str(random()).encode("utf8")).hexdigest()[:6]
    user.activation_key = hashlib.sha1(
        (user.email + salt).encode("utf8")
    ).hexdigest()
    user.activation_key_expires = default_key_expires()
    user.save()
    verify_link = reverse("auth:verify", args=[user.email, user.activation_key])
    title = f"ПЕРСПЕКТИВА. Подтверждение электронной почты"
    message = f"Для подтверждения учетной записи {user.username}  \
    перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}"
    return send_mail(
        title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False
    )


def send_verify_mail_again(request, email):
    user = get_object_or_404(SiteUser, email=email)
    if not user.is_verified and not user.is_activation_key_too_young(5):
        send_verify_mail(user)
        context = {"user": user}
        return render(request, "authapp/verification_sent.html", context=context)
    else:
        return HttpResponseRedirect('/')


class SiteUserRegisterView(CreateView):
    """
    Контроллер регистрации
    """
    Model = SiteUser
    form_class = SiteUserRegistrationForm
    template_name = "authapp/registration.html"
    success_url = reverse_lazy("authapp:login")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        send_verify_mail(user)
        context = {"user": user}
        return render(self.request, "authapp/verification_sent.html", context=context)

    def verify(self, email, activation_key):
        try:
            user = SiteUser.objects.get(email=email)
            if (
                user.activation_key == activation_key
                and not user.is_activation_key_expired()
            ):
                user.is_verified = True
                user.save()
                auth.login(
                    self, user, backend="django.contrib.auth.backends.ModelBackend"
                )
            return render(self, "authapp/verification.html")
        except Exception as e:
            print(e.with_traceback())
            return HttpResponseRedirect(reverse("index"))


class SiteUserLoginView(LoginView):
    """
    Контроллер аутентификации
    """
    Model = SiteUser
    form_class = SiteUserLoginForm
    template_name = "authapp/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("index")

    def form_valid(self, form):
        user = get_object_or_404(SiteUser, username=form["username"].value())
        if not user.is_verified:
            return render(self.request, 'authapp/verification_not_passed.html', context={'user': user})
        return super().form_valid(form)


class SiteUserLogoutView(LogoutView):
    """
    Контроллер выхода из системы
    """
    model = SiteUser
    login_url = reverse_lazy("auth:login")
    next_page = reverse_lazy("index")
