from django.urls import path, re_path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact_us", views.contact_us, name="contact-us"),
    path("post_requirment", views.post_requirment, name="post-requirment"),

    # product
    path("products/<int:main_category_id>", views.products, name="products"),
    path("product_details/<int:pk>", views.product_details, name="product-details"),

    # wishlist
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_wishlist/", views.add_wishlist, name="add-wishlist"),
    path("remove_wishlist/<int:pk>", views.remove_wishlist, name="remove-wishlist"),

    # cart
    path("cart/", views.cart, name="cart"),
    path("add_cart/", views.add_cart, name="add-cart"),
    path("update_cart/", views.update_cart, name="update-cart"),
    path("remove_cart/<int:pk>", views.remove_cart, name="remove-cart"),

    # my account
    path("checkout/", views.checkout, name="checkout"),
    path("my_account/", views.my_account, name="my_account"),
    path("address/", views.address, name="address"),
    path("login_security/", views.login_security, name="login-security"),
    path("offers", views.offers, name="offers"),
]
