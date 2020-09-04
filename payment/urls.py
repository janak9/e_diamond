from django.urls import path
from payment import views

app_name = "payment"

urlpatterns = [
    path("confirm/<int:pk>", views.confirm, name="confirm"),
    path("success/<int:pk>", views.success, name="success"),
    path("failure/<int:pk>", views.failure, name="failure"),
]
