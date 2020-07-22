from django.shortcuts import render, redirect
from product.models import MainCategory, Category, SubCategory

def get_common_context(context):
    context['test'] = 'test'
    context['main_categories'] = MainCategory.objects.all()
    context['categories'] = Category.objects.all()
    context['sub_categories'] = SubCategory.objects.all()

def home(request):
    context = {}
    context['active'] = 'home'
    get_common_context(context)
    return render(request, 'user/index.html', context)


def product(request):
    return render(request, 'user/index.html', {'title': 'test'})
