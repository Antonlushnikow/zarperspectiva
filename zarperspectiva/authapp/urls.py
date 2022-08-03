from django.urls import path

from authapp.views import (
    SiteUserLoginView,
    SiteUserLogoutView,
    SiteUserRegisterView,
    SiteUserUpdateView,
    SiteUserPasswordResetView,
    send_verify_mail_again,
    ProfileView,
    StudentCreateView,
    StudentEditView,
    StudentDeleteView,
    TermsConditionsView,
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
    path("send-verify/<str:email>", send_verify_mail_again, name="send-verify"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("update-profile/", SiteUserUpdateView.as_view(), name="update-profile"),

    path("create-student/", StudentCreateView.as_view(), name="create-student"),
    path("update-student/<int:pk>/", StudentEditView.as_view(), name="update-student"),
    path("delete-student/<int:pk>/", StudentDeleteView.as_view(), name="delete-student"),

    path("terms-conditions/", TermsConditionsView.as_view(), name="terms-conditions"),
]
