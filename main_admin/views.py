from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decouple import config
from auth_user.decorator import checkLogin
from base import const
from product.models import MainCategory, Category, SubCategory, AdditionalInformation, Product, Review
from main_admin.models import Image, SocialLink, Contact, AboutUs, Details, Offer
from main_admin.forms import ImageFormset
import traceback

def get_common_context(request, context):
    context['app_name'] = config('APP_NAME')
    context['CONST'] = const

@checkLogin('admin')
def dashboard(request):
    context = {}
    context['active'] = 'dashboard'
    get_common_context(request, context)
    return render(request, 'main_admin/index.html', context)

@checkLogin('admin')
def add_main_category(request, pk=None):
    context = {}
    context['active'] = 'main_category'
    get_common_context(request, context)
    if pk is not None:
        context['task'] = "Edit"
        context['main_category'] = MainCategory.objects.get(id=pk)
    else:
        context['task'] = "Add"

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp)) # remove extra fields
            if pk is not None:
                MainCategory.objects.filter(pk=pk).update(**data)
            else:
                MainCategory.objects.create(**data)
            return redirect("main_admin:view-main-category")
    except Exception as err:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'main_admin/add_main_category.html', context)

@checkLogin('admin')
def view_main_category(request):
    context = {}
    context['active'] = 'main_category'
    get_common_context(request, context)
    
    main_category_list = MainCategory.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(main_category_list, 5)
    try:
        main_categories = paginator.page(page)
    except PageNotAnInteger:
        main_categories = paginator.page(1)
    except EmptyPage:
        main_categories = paginator.page(paginator.num_pages)
    context['main_categories'] = main_categories
    return render(request, 'main_admin/view_main_category.html', context)

@checkLogin('admin')
def del_main_category(request, pk):
    main_category = MainCategory.objects.get(pk=pk)
    main_category.delete()
    return redirect("main_admin:view-main-category")


@checkLogin('admin')
def add_category(request, pk=None):
    context = {}
    context['active'] = 'category'
    get_common_context(request, context)
    context['main_categories'] = MainCategory.objects.all().order_by('-id')
    if pk is not None:
        context['task'] = "Edit"
        context['category'] = Category.objects.get(id=pk)
        context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    else:
        context['task'] = "Add"
        context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken', 'form-TOTAL_FORMS', 'form-INITIAL_FORMS', 'form-MIN_NUM_FORMS', 'form-MAX_NUM_FORMS', 'form-0-src']

            if context['image_form'].is_valid():
                for form in context['image_form']:
                    if form.cleaned_data.get('src'):
                        if pk is not None:
                            image = context['category'].image
                            image.src = form.cleaned_data.get('src')
                            image.save()
                        else:
                            image = form.save()
                        data['image_id'] = image.pk

                list(map(data.pop, tmp)) # remove extra fields
                if pk is not None:
                    Category.objects.filter(pk=pk).update(**data)
                else:
                    Category.objects.create(**data)
                return redirect("main_admin:view-category")
    except Exception as err:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'main_admin/add_category.html', context)

@checkLogin('admin')
def view_category(request):
    context = {}
    context['active'] = 'category'
    get_common_context(request, context)
    
    category_list = Category.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(category_list, 5)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    context['categories'] = categories
    return render(request, 'main_admin/view_category.html', context)

@checkLogin('admin')
def del_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect("main_admin:view-category")


# sub category
@checkLogin('admin')
def add_sub_category(request, pk=None):
    context = {}
    context['active'] = 'sub_category'
    get_common_context(request, context)
    context['main_categories'] = MainCategory.objects.all().order_by('-id')
    if pk is not None:
        context['task'] = "Edit"
        context['sub_category'] = Category.objects.get(id=pk)
        context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    else:
        context['task'] = "Add"
        context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken', 'form-TOTAL_FORMS', 'form-INITIAL_FORMS', 'form-MIN_NUM_FORMS', 'form-MAX_NUM_FORMS']

            if context['image_form'].is_valid():
                for form in context['image_form']:
                    if pk is not None:
                        image = context['sub_category'].image
                        image.src = form.cleaned_data.get('src')
                        image.save()
                    else:
                        image = form.save()
                    data['image_id'] = image.pk

                list(map(data.pop, tmp)) # remove extra fields
                if pk is not None:
                    Category.objects.filter(pk=pk).update(**data)
                else:
                    Category.objects.create(**data)
                return redirect("main_admin:view-sub-category")
    except Exception as err:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'main_admin/add_sub_category.html', context)

@checkLogin('admin')
def view_sub_category(request):
    context = {}
    context['active'] = 'sub_category'
    get_common_context(request, context)
    
    sub_category_list = Category.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(sub_category_list, 5)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    context['categories'] = categories
    return render(request, 'main_admin/view_sub_category.html', context)

@checkLogin('admin')
def del_sub_category(request, pk):
    sub_category = Category.objects.get(pk=pk)
    sub_category.delete()
    return redirect("main_admin:view-sub-category")
