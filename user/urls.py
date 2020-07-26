from django.urls import path, re_path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact_us", views.contact_us, name="contact-us"),
    path("products/<int:main_category_id>", views.products, name="products"),
    path("product_details/<int:pk>", views.product_details, name="product-details"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_wishlist/", views.add_wishlist, name="add-wishlist"),
    path("remove_wishlist/<int:pk>", views.remove_wishlist, name="remove-wishlist"),
    path("cart/", views.cart, name="cart"),
    path("add_cart/", views.add_cart, name="add-cart"),
    path("remove_cart/<int:pk>", views.remove_cart, name="remove-cart"),
]
