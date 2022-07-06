from django.urls import path

import authapp.views as authapp

from authapp.views import (
    SiteUserLoginView,
    SiteUserLogoutView,
    SiteUserRegisterView,
    send_verify_mail_again,
)

urlpatterns = [
    path("login/", SiteUserLoginView.as_view(), name="login"),
    path("logout/", SiteUserLogoutView.as_view(), name="logout"),
    path("register/", SiteUserRegisterView.as_view(), name="register"),
    path(
        "verify/<str:email>/<str:activation_key>/",
        SiteUserRegisterView.verify,
        name="verify",
    ),
    path("send-verify/<str:email>", send_verify_mail_again, name="send-verify")
]