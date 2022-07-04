from django.urls import path

import authapp.views as authapp

from .views import (
    SiteUserLoginView,
    SiteUserLogoutView,
    SiteUserRegisterView,
)

urlpatterns = [
    path("login/", SiteUserLoginView.as_view(), name="login"),
    path("logout/", SiteUserLogoutView.as_view(), name="logout"),
    path("register/", SiteUserRegisterView.as_view(), name="register"),
    path(
        "verify/<str:email>/<str:activation_key>/",
        authapp.SiteUserRegisterView.verify,
        name="verify",
    ),
]