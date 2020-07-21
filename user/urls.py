from django.urls import path, re_path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
]
