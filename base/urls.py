from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from decouple import config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_user.urls', namespace="auth")),
    path('main_admin/', include('main_admin.urls', namespace="main_admin")),
    path('', include('user.urls', namespace="user")),
    path('product/', include('product.urls', namespace="product")),
    path('payment/', include('payment.urls', namespace="payment")),
]

AdminSite.site_header = config('APP_NAME')
AdminSite.site_title = config('APP_NAME')

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
