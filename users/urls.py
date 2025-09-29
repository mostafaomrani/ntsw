from django.urls import path

from .views import (
    RegisterView,
    VerifyPhoneView,
    SelectVerificationMod,
    SendResetCodeView,
    ResetPasswordView,
)

from django.contrib.auth.views import LoginView, LogoutView


app_name = 'users'

urlpatterns = [
    path("login/", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('select-verification-mod/<uuid:user_uuid>',
         SelectVerificationMod.as_view(), name='select_verification_mod'),
    path('verify-phone/<uuid:user_uuid>',
         VerifyPhoneView.as_view(), name='verify_phone'),
    path('send-reset-code/', SendResetCodeView.as_view(), name='send_reset_code'),
    path('reset-password/<str:username>/',
         ResetPasswordView.as_view(), name='password_reset_confirm'),



    # path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    # path(
    # "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    # ),
    # path(
    # "password_change/done/",
    # views.PasswordChangeDoneView.as_view(),
    # name="password_change_done",
    # ),

    # path(
    # "password_reset/done/",
    # views.PasswordResetDoneView.as_view(),
    # name="password_reset_done",
    # ),
    # path(
    # "reset/<uidb64>/<token>/",
    # views.PasswordResetConfirmView.as_view(),
    # name="password_reset_confirm",
    # ),
    # path(
    # "reset/done/",
    # views.PasswordResetCompleteView.as_view(),
    # name="password_reset_complete",
    # ),
]
