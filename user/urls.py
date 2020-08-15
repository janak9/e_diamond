from django.urls import path, re_path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("return_policy", views.return_policy, name="return-policy"),
    path("contact_us", views.contact_us, name="contact-us"),
    path("post_requirment", views.post_requirment, name="post-requirment"),
    path("feedback", views.feedback, name="feedback"),

    # product
    path("products/<int:main_category_id>", views.products, name="products"),
    path("product_details/<int:pk>", views.product_details, name="product-details"),
    path("product_details/description/<int:pk>", views.description, name="description"),
    path("add_review/", views.add_review, name="add-review"),

    # wishlist
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_wishlist/", views.add_wishlist, name="add-wishlist"),
    path("remove_wishlist/<int:pk>", views.remove_wishlist, name="remove-wishlist"),

    # cart
    path("cart/", views.cart, name="cart"),
    path("add_cart/", views.add_cart, name="add-cart"),
    path("update_cart/", views.update_cart, name="update-cart"),
    path("remove_cart/<int:pk>", views.remove_cart, name="remove-cart"),

    # compare
    path("compare", views.compare, name="compare"),
    path("add_compare/", views.add_compare, name="add-compare"),
    path("remove_compare/<int:product_id>", views.remove_compare, name="remove-compare"),

    # my account
    path("checkout/", views.checkout, name="checkout"),
    path("my_account/", views.my_account, name="my_account"),
    path("login_security/", views.login_security, name="login-security"),
    path("offers", views.offers, name="offers"),
    path("address/", views.address, name="address"),
    path("orders", views.orders, name="orders"),
    path("payments", views.payments, name="payments"),
    path("invoice/<int:pk>", views.invoice, name="invoice"),
]
