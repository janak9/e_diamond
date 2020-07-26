from django.urls import path, re_path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact_us", views.contact_us, name="contact-us"),
    path("products/<int:main_category_id>", views.products, name="products"),
    path("product_details/<int:pk>", views.product_details, name="product-details"),
]
