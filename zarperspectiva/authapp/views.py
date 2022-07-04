# from allauth.account.signals import user_signed_up
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
from .models import SiteUser


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
        self.send_verify_mail(user)
        context = {}
        context["user"] = user
        return render(self.request, "authapp/verification_sent.html", context=context)

    def send_verify_mail(self, user):
        verify_link = reverse("auth:verify", args=[user.email, user.activation_key])
        title = f"Подтверждение учетной записи {user.username} на портале Site"
        message = f"Для подтверждения учетной записи {user.username} на портале \
        {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}"
        send_mail(
            title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False
        )

    def verify(self, email, activation_key):
        try:
            user = SiteUser.objects.get(email=email)
            if (
                user.activation_key == activation_key
                and not user.is_activation_key_expired()
            ):
                user.is_active = True
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SiteUserLoginView, self).get_context_data()
        context["title"] = "авторизация"
        """
        После вызова предка get_context_data в контексте лежит форма с состоянием valid=Undefined. По-этому она снова 
        валидируется и второй раз запрашивается у гугл капчи проверка, которая проваливается, тк токен на форме еще не
        обновился но уже для него была сделана проверка. В то же время в kwargs лежит форма с определнным состоянием, и
        для нее уже все проверки пройдены. Перекладываем форму из kwargs в контекст и передаем рендеру. 
        """
        if kwargs:
            context["form"] = kwargs["form"]
        return context

    def form_valid(self, form):
        user = get_object_or_404(SiteUser, username=form["username"].value())
        if user.is_deleted:
            return HttpResponseNotFound("Пользователь удален")
        if user.is_blocked:
            return HttpResponseNotFound(
                f"Пользователь заблокирован до {user.block_expires}"
            )
        return super(SiteUserLoginView, self).form_valid(form)


class SiteUserLogoutView(LogoutView):
    """
    Контроллер выхода из системы
    """
    model = SiteUser
    login_url = reverse_lazy("auth:login")