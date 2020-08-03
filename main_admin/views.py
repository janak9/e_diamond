from django.shortcuts import render
from auth_user.decorator import checkLogin
from decouple import config

def get_common_context(request, context):
    context['app_name'] = config('APP_NAME')

@checkLogin('admin')
def dashboard(request):
    context = {}
    context['active'] = 'dashboard'
    get_common_context(request, context)
    return render(request, 'main_admin/index.html', context)

