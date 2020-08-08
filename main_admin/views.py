from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decouple import config
from auth_user.decorator import checkLogin
from base import const
from product.models import MainCategory, Category, SubCategory, AdditionalInformation, Product, Review
from main_admin.models import Image, SocialLink, Contact, AboutUs, Details, Offer
from main_admin.forms import ImageFormset
import traceback
import json

def get_common_context(request, context):
    context['app_name'] = config('APP_NAME')
    context['CONST'] = const

@checkLogin('admin')
def dashboard(request):
    context = {}
    context['active'] = 'dashboard'
    get_common_context(request, context)
    return render(request, 'main_admin/index.html', context)

# main category
@checkLogin('admin')
def add_main_category(request, pk=None):
    context = {}
    context['active'] = 'main_category'
    get_common_context(request, context)
    if pk is not None:
        context['task'] = "Edit"
        context['main_category'] = MainCategory.all_objects.get(id=pk)
    else:
        context['task'] = "Add"

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp)) # remove extra fields
            if pk is not None:
                MainCategory.all_objects.filter(pk=pk).update(**data)
            else:
                MainCategory.all_objects.create(**data)
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
    main_category_list = MainCategory.all_objects.all().order_by('-id')
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
    main_category = MainCategory.all_objects.get(pk=pk)
    main_category.delete()
    return redirect("main_admin:view-main-category")


# category
@csrf_exempt
@checkLogin('admin')
def get_category(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        main_category_id = data['main_category_id']
        categories = Category.all_objects.filter(main_category_id=main_category_id).order_by('name').values()
        result['status'] = 'success'
        result['categories'] = list(categories)
    except Exception as err:
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))

@checkLogin('admin')
def add_category(request, pk=None):
    context = {}
    context['active'] = 'category'
    get_common_context(request, context)
    context['main_categories'] = MainCategory.all_objects.all().order_by('name')
    if pk is not None:
        context['task'] = "Edit"
        context['category'] = Category.all_objects.get(id=pk)
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
                    if form.cleaned_data.get('src'):
                        if pk is not None:
                            image = context['category'].image
                            image.src = form.cleaned_data.get('src')
                            image.save()
                        else:
                            image = form.save()
                        data['image_id'] = image.pk
                    else:
                        tmp.append('form-0-src')

                list(map(data.pop, tmp)) # remove extra fields
                if pk is not None:
                    Category.all_objects.filter(pk=pk).update(**data)
                else:
                    Category.all_objects.create(**data)
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
    
    category_list = Category.all_objects.all().order_by('-id')
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
    category = Category.all_objects.get(pk=pk)
    category.delete()
    return redirect("main_admin:view-category")


# sub category
@csrf_exempt
@checkLogin('admin')
def get_sub_category(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        category_id = data['category_id']
        sub_categories = SubCategory.all_objects.filter(category_id=category_id).order_by('name').values()
        result['status'] = 'success'
        result['sub_categories'] = list(sub_categories)
    except Exception as err:
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))

@checkLogin('admin')
def add_sub_category(request, pk=None):
    context = {}
    context['active'] = 'sub_category'
    get_common_context(request, context)
    context['main_categories'] = MainCategory.all_objects.all().order_by('name')
    if pk is not None:
        context['task'] = "Edit"
        context['sub_category'] = SubCategory.all_objects.get(id=pk)
        context['categories'] = Category.all_objects.filter(main_category_id=context['sub_category'].main_category_id).order_by('name')
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
                    if form.cleaned_data.get('src'):
                        if pk is not None:
                            image = context['sub_category'].image
                            image.src = form.cleaned_data.get('src')
                            image.save()
                        else:
                            image = form.save()
                        data['image_id'] = image.pk
                    else:
                        tmp.append('form-0-src')

                list(map(data.pop, tmp)) # remove extra fields
                if pk is not None:
                    SubCategory.all_objects.filter(pk=pk).update(**data)
                else:
                    SubCategory.all_objects.create(**data)
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
    
    sub_category_list = SubCategory.all_objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(sub_category_list, 5)
    try:
        sub_categories = paginator.page(page)
    except PageNotAnInteger:
        sub_categories = paginator.page(1)
    except EmptyPage:
        sub_categories = paginator.page(paginator.num_pages)
    context['sub_categories'] = sub_categories
    return render(request, 'main_admin/view_sub_category.html', context)

@checkLogin('admin')
def del_sub_category(request, pk):
    sub_category = SubCategory.all_objects.get(pk=pk)
    sub_category.delete()
    return redirect("main_admin:view-sub-category")

# product
@checkLogin('admin')
def add_product(request, pk=None):
    context = {}
    context['active'] = 'product'
    get_common_context(request, context)
    context['main_categories'] = MainCategory.all_objects.all().order_by('name')
    context['cnt'] = 1
    if pk is not None:
        context['task'] = "Edit"
        context['product'] = Product.all_objects.get(id=pk)
        context['cnt'] = context['product'].additional_information.all().count()
        context['categories'] = Category.all_objects.filter(main_category_id=context['product'].main_category_id).order_by('name')
        context['sub_categories'] = SubCategory.all_objects.filter(category_id=context['product'].category_id).order_by('name')
        context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    else:
        context['task'] = "Add"
        context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            product_data = {
                'main_category_id': data['main_category_id'],
                'category_id': data['category_id'],
                'sub_category_id': data['sub_category_id'],
                'title': data['title'],
                'description': data['description'],
                'qty': data['qty'],
                'available_qty': data['available_qty'],
                'price': data['price'],
                'status': data['status'],
            }

            # Additional Informations
            new_info = { k:v for k,v in data.items() if k.startswith('new_info') }
            old_info = { k:v for k,v in data.items() if k.startswith('info_') }
            result_new = {}
            for key, value in new_info.items():
                no = key.split('_')[-1]
                field = key.split('_')[-2]
                if no not in result_new:
                    result_new[no] = {}
                result_new[no][field] = value
            
            result_old = {}
            for key, value in old_info.items():
                no = key.split('_')[-1]
                field = key.split('_')[-2]
                if no not in result_old:
                    result_old[no] = {}
                result_old[no][field] = value
            
            for key, value in result_new.items():
                info = AdditionalInformation.objects.create(**value)
                context['product'].additional_information.add(info)

            for info in context['product'].additional_information.all():
                key = str(info.pk)
                if key in [*result_old]:
                    info.title = result_old[key]['title']
                    info.description = result_old[key]['description']
                    info.save()
                else:
                    context['product'].additional_information.remove(info)
            context['product'].save()

            if context['image_form'].is_valid():
                images = []
                for form in context['image_form']:
                    if form.cleaned_data.get('src'):
                        if pk is not None:
                            # image = context['product'].images.all()
                            # image[0].src = form.cleaned_data.get('src')
                            # image[0].save()
                            image = form.save()
                            pass
                        else:
                            image = form.save()
                        images.append(image)
                    else:
                        tmp.append('form-0-src')

                if pk is not None:
                    product = Product.all_objects.filter(pk=pk)
                    product.update(**data)
                    product.get().images.set(images)
                else:
                    product = Product.all_objects.create(**data)
                    product.save()
                    product.images.set(images)
                return redirect("main_admin:view-product")
    except Exception as err:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'main_admin/add_product.html', context)

@checkLogin('admin')
def view_product(request):
    context = {}
    context['active'] = 'product'
    get_common_context(request, context)
    
    product_list = Product.all_objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 5)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context['products'] = products
    return render(request, 'main_admin/view_product.html', context)

@checkLogin('admin')
def del_product(request, pk):
    product = Product.all_objects.get(pk=pk)
    product.delete()
    return redirect("main_admin:view-product")
