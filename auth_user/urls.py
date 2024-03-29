from django.urls import path, re_path
from auth_user import views

app_name = "auth_user"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("resend_verify/", views.resend_verification_token, name="resend-verify"),
    re_path(r'^verify_email/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-]+)$',
            views.verify_account, name='verify-email'),

    path("profile/", views.profile, name="profile"),
    path("forgot_pwd/", views.forgot_pwd, name="forgot-pwd"),
    re_path(r'^verify_forgot_pwd/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-]+)$',
            views.verify_forgot_password, name='verify-forgot-password'),
    path("change_pwd/", views.change_password, name="change-pwd"),
]
