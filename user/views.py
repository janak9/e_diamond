from django.shortcuts import render, redirect
from product.models import MainCategory, Category, SubCategory, Product
from main_admin.models import Image, AboutUs

def get_common_context(context):
    context['test'] = 'test'
    context['main_categories'] = MainCategory.objects.all()
    context['categories'] = Category.objects.all()
    context['about_us'] = AboutUs.objects.all()[0]
    context['top_10_products'] = Product.objects.order_by("-timestamp")[:10]

def home(request):
    context = {}
    context['active'] = 'home'
    get_common_context(context)
    return render(request, 'user/index.html', context)


def about(request):
    context = {}
    context['active'] = 'about'
    get_common_context(context)
    return render(request, 'user/about.html', context)
