from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from decouple import config

urlpatterns = [
    path('admin/', admin.site.urls),
]

AdminSite.site_header = config('APP_NAME')
AdminSite.site_title = config('APP_NAME')

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)