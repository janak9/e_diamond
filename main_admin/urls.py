from django.urls import path, re_path, include
from main_admin import views
from base import const

app_name = "main_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("test_mail", views.test_mail, name="test_mail"),

    path('main_category/', include([
        path('', views.add_main_category, name="add-main-category"),
        path('<int:pk>', views.add_main_category, name="edit-main-category"),
        path('view', views.view_main_category, name="view-main-category"),
        path('delete/<int:pk>', views.del_main_category, name="del-main-category"),
    ])),
    
    path("get_category/", views.get_category, name="get-category"),
    path('category/', include([
        path('', views.add_category, name="add-category"),
        path('<int:pk>', views.add_category, name="edit-category"),
        path('view', views.view_category, name="view-category"),
        path('delete/<int:pk>', views.del_category, name="del-category"),
    ])),

    path("get_sub_category/", views.get_sub_category, name="get-sub-category"),
    path('sub_category/', include([
        path('', views.add_sub_category, name="add-sub-category"),
        path('<int:pk>', views.add_sub_category, name="edit-sub-category"),
        path('view', views.view_sub_category, name="view-sub-category"),
        path('delete/<int:pk>', views.del_sub_category, name="del-sub-category"),
    ])),
    
    path('product/', include([
        path('', views.add_product, name="add-product"),
        path('<int:pk>', views.add_product, name="edit-product"),
        path('view', views.view_product, name="view-product"),
        path('delete/<int:pk>', views.del_product, name="del-product"),
    ])),

    path("post_requirements/", views.view_post_requirements, name="view-post-requirements"),
    path("contact_us/", views.view_contact_us, name="view-contact-us"),
    path("edit_contact/<int:pk>/<int:contact_type>", views.edit_contact, name="edit-contact"),
    path("contact/<int:pk>/<int:contact_type>", views.del_contact, name="del-contact"),
    path("orders/", views.view_orders, name="view-orders"),
    path("payments/", views.view_payments, name="view-payments"),
    path("reviews/", views.view_reviews, name="view-reviews"),
    path("about_us/", views.edit_about_us, name="edit-about-us"),
    path("details/<int:detail_type>", views.edit_details, name="edit-details"),
]
