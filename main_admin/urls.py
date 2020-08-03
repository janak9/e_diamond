from django.urls import path, re_path
from main_admin import views

app_name = "main_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
