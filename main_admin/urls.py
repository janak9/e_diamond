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

    path('user/', include([
        path('<int:pk>', views.edit_user, name="edit-user"),
        path('view', views.view_user, name="view-user"),
        path('delete/<int:pk>', views.del_user, name="del-user"),
    ])),

    path('reviews/', include([
        path('<int:pk>', views.edit_review, name="edit-review"),
        path('view', views.view_reviews, name="view-reviews"),
        path('delete/<int:pk>', views.del_review, name="del-review"),
    ])),

    path('feedback/', include([
        path('<int:pk>', views.edit_feedback, name="edit-feedback"),
        path('view', views.view_feedbacks, name="view-feedbacks"),
        path('delete/<int:pk>', views.del_feedback, name="del-feedback"),
    ])),

    path('contact/', include([
        path('<int:contact_type>/<int:pk>', views.edit_contact, name="edit-contact"),
        path('view/<int:contact_type>', views.view_contact, name="view-contact"),
        path('delete/<int:contact_type>/<int:pk>', views.del_contact, name="del-contact"),
    ])),

    path("orders/", views.view_orders, name="view-orders"),
    path("payments/", views.view_payments, name="view-payments"),
    path("about_us/", views.edit_about_us, name="edit-about-us"),
    path("details/<int:detail_type>", views.edit_details, name="edit-details"),
]
