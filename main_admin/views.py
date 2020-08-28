from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decouple import config
from auth_user.models import User as user_model
from auth_user.decorator import checkLogin
from base import const, mail, settings
from user.models import Order, Feedback
from product.models import MainCategory, Category, SubCategory, AdditionalInformation, Product, Review
from payment.models import PaymentOrder, Payment
from main_admin.models import Image, SocialLink, Contact, AboutUs, Details, Offer
from main_admin.forms import ImageFormset, AboutForm
import traceback
import json

def get_common_context(request, context):
    context['app_name'] = config('APP_NAME')
    context['CONST'] = const

def test_mail(request):
    user = user_model.objects.filter(user_type=const.ADMIN)
    payment_order = PaymentOrder.objects.get(pk=25)
    about_us = AboutUs.objects.first()
    mail.send_email(user, "order_admin", payment_order=payment_order)
    mail.send_email(payment_order.user, "order_user", payment_order=payment_order)
    return HttpResponse("sent")
    # data = {
    #         'user': payment_order.user,
    #         'app_name': config('APP_NAME'),
    #         'base_url': settings.SITE_URL,
    #         'about_us': about_us,
    #         'payment_order': payment_order
    #     }
    # return render(request, 'mail/order_user.html', data)

@checkLogin('admin')
def dashboard(request):
    context = {}
    context['active'] = 'dashboard'
    get_common_context(request, context)
    context['user_count'] = len(user_model.objects.all())
    context['product_count'] = len(Product.objects.all())
    context['order_count'] = len(Order.objects.all())
    context['payment_count'] = len(Payment.objects.all())
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
    context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    if pk is not None:
        context['task'] = "Edit"
        context['category'] = Category.all_objects.get(id=pk)
    else:
        context['task'] = "Add"

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
    context['image_form'] = ImageFormset(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    if pk is not None:
        context['task'] = "Edit"
        context['sub_category'] = SubCategory.all_objects.get(id=pk)
        context['categories'] = Category.all_objects.filter(main_category_id=context['sub_category'].main_category_id).order_by('name')
    else:
        context['task'] = "Add"

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
    if pk is not None:
        context['task'] = "Edit"
        context['product'] = Product.all_objects.get(id=pk)
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

            images = []
            for form in context['image_form']:
                print(form)
                print(form.cleaned_data)
                image_data = form.cleaned_data
                image = image_data.get('id')
                print(image)
                if image_data.get('src') or image:
                    if image and image_data.get('src'):
                        image.src = image_data.get('src')
                        image.save()
                    elif not image:
                        image = form.save()
                    images.append(image)

            if pk is not None:
                product = Product.all_objects.filter(pk=pk)
                product.update(**product_data)
                product = product.get()
                old = [image.pk for image in product.images.all()]
                new = [image.pk for image in images]
                removed_img = list(set(old) - set(new))
                for img_pk in removed_img:
                    img = Image.objects.get(pk=img_pk)
                    img.delete()
                product.images.set(images)
            else:
                product = Product.all_objects.create(**product_data)
                product.save()
                product.images.set(images)
            
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
            
            # save
            for info in product.additional_information.all():
                key = str(info.pk)
                if key in [*result_old]:
                    info.title = result_old[key]['title']
                    info.description = result_old[key]['description']
                    info.save()
                else:
                    product.additional_information.remove(info)
            
            for key, value in result_new.items():
                info = AdditionalInformation.objects.create(**value)
                product.additional_information.add(info)

            # Social Link
            new_social = { k:v for k,v in data.items() if k.startswith('new_social') }
            old_social = { k:v for k,v in data.items() if k.startswith('social_') }
            result_new = {}
            for key, value in new_social.items():
                no = key.split('_')[-1]
                field = key.split('_')[-2]
                if no not in result_new:
                    result_new[no] = {}
                result_new[no][field] = value
            
            result_old = {}
            for key, value in old_social.items():
                no = key.split('_')[-1]
                field = key.split('_')[-2]
                if no not in result_old:
                    result_old[no] = {}
                result_old[no][field] = value
            
            del result_old['id'] # remove social_link_id
            # save
            for social in product.social_links.all():
                key = str(social.pk)
                if key in [*result_old]:
                    social.social_icon = result_old[key]['icon']
                    social.link = result_old[key]['link']
                    social.save()
                else:
                    product.social_links.remove(social)

            for key, value in result_new.items():
                social = SocialLink.objects.create(social_icon= value['icon'], link=value['link'])
                product.social_links.add(social)
            product.save()

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


# offer
@checkLogin('admin')
def add_offer(request, pk=None):
    context = {}
    context['active'] = 'offer'
    get_common_context(request, context)
    if pk is not None:
        context['task'] = "Edit"
        context['offer'] = Offer.all_objects.get(id=pk)
    else:
        context['task'] = "Add"

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp)) # remove extra fields
            data['code'] = data['code'].upper()
            if pk is not None:
                Offer.all_objects.filter(pk=pk).update(**data)
            else:
                Offer.all_objects.create(**data)
            return redirect("main_admin:view-offer")
    except Exception as err:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'main_admin/add_offer.html', context)

@checkLogin('admin')
def view_offer(request):
    context = {}
    context['active'] = 'offer'
    get_common_context(request, context)
    
    offer_list = Offer.all_objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(offer_list, 5)
    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)
    context['offers'] = offers
    return render(request, 'main_admin/view_offer.html', context)

@checkLogin('admin')
def del_offer(request, pk):
    offer = Offer.all_objects.get(pk=pk)
    offer.delete()
    return redirect("main_admin:view-offer")


# user
@checkLogin('admin')
def view_user(request):
    context = {}
    context['active'] = 'user'
    get_common_context(request, context)
    user_list = user_model.all_objects.filter(user_type=const.USER).order_by('-date_joined')
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context['users'] = users
    return render(request, 'main_admin/view_users.html', context)

@checkLogin('admin')
def edit_user(request, pk):
    context = {}
    context['active'] = 'user'
    get_common_context(request, context)
    context['user_detail'] = user_model.all_objects.get(pk=pk)
    if (request.method == 'POST'):
        if 'status' in request.POST:
            context['user_detail'].status = request.POST['status']
            context['user_detail'].save()
            return redirect("main_admin:view-user")
    return render(request, 'main_admin/edit_user.html', context)

@checkLogin('admin')
def del_user(request, pk):
    user = user_model.all_objects.get(pk=pk)
    user.delete()
    return redirect("main_admin:view-user")


# contact
@checkLogin('admin')
def view_contact(request, contact_type=const.CONTACT_US):
    context = {}
    context['active'] = 'contact_us' if contact_type is const.CONTACT_US else 'post_requirements'
    get_common_context(request, context)
    context['contact_type'] = contact_type
    contact_list = Contact.objects.filter(contact_type=contact_type).order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(contact_list, 5)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context['contacts'] = contacts
    return render(request, 'main_admin/view_contacts.html', context)

@checkLogin('admin')
def edit_contact(request, contact_type, pk):
    context = {}
    context['active'] = 'contact_us'
    get_common_context(request, context)
    context['contact'] = Contact.objects.get(pk=pk)
    if (request.method == 'POST'):
        if 'status' in request.POST:
            context['contact'].status = request.POST['status']
            context['contact'].save()
            return redirect("main_admin:view-contact", contact_type=contact_type)
        if 'reply' in request.POST:
            mail.send_email(None, 'contact_reply', contact=context['contact'], reply=request.POST['reply'])
            context['msg'] = 'mail sent to user\'s email ' + context['contact'].email
    return render(request, 'main_admin/edit_contact.html', context)

@checkLogin('admin')
def del_contact(request, contact_type, pk):
    contact = Contact.objects.get(pk=pk)
    contact.delete()
    return redirect("main_admin:view-contact", contact_type=contact_type)


# review
@checkLogin('admin')
def view_reviews(request):
    context = {}
    context['active'] = 'reviews'
    get_common_context(request, context)
    
    review_list = Review.all_objects.all().order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(review_list, 5)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    context['reviews'] = reviews
    return render(request, 'main_admin/view_reviews.html', context)

@checkLogin('admin')
def edit_review(request, pk):
    context = {}
    context['active'] = 'reviews'
    get_common_context(request, context)
    context['review'] = Review.all_objects.get(pk=pk)
    if (request.method == 'POST'):
        if 'status' in request.POST:
            context['review'].status = request.POST['status']
            context['review'].save()
            return redirect("main_admin:view-reviews")
    return render(request, 'main_admin/edit_review.html', context)

@checkLogin('admin')
def del_review(request, pk):
    review = Review.all_objects.get(pk=pk)
    review.delete()
    return redirect("main_admin:view-reviews")


# feedback
@checkLogin('admin')
def view_feedbacks(request):
    context = {}
    context['active'] = 'feedbacks'
    get_common_context(request, context)
    
    feedback_list = Feedback.all_objects.all().order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(feedback_list, 5)
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)
    context['feedbacks'] = feedbacks
    return render(request, 'main_admin/view_feedbacks.html', context)

@checkLogin('admin')
def edit_feedback(request, pk):
    context = {}
    context['active'] = 'feedbacks'
    get_common_context(request, context)
    context['feedback'] = Feedback.all_objects.get(pk=pk)
    if (request.method == 'POST'):
        if 'status' in request.POST:
            context['feedback'].status = request.POST['status']
            context['feedback'].read_status = request.POST['read_status']
            context['feedback'].save()
            return redirect("main_admin:view-feedbacks")
    return render(request, 'main_admin/edit_feedback.html', context)

@checkLogin('admin')
def del_feedback(request, pk):
    feedback = Feedback.all_objects.get(pk=pk)
    feedback.delete()
    return redirect("main_admin:view-feedbacks")


# payments
@checkLogin('admin')
def view_payments(request):
    context = {}
    context['active'] = 'payments'
    get_common_context(request, context)
    payment_list = Payment.objects.all().order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(payment_list, 5)
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)
    context['payments'] = payments
    return render(request, 'main_admin/view_payments.html', context)

@checkLogin('admin')
def edit_payment(request, pk):
    context = {}
    context['active'] = 'payments'
    get_common_context(request, context)
    context['payment'] = Payment.objects.get(pk=pk)
    if (request.method == 'POST'):
        if 'track_order_status' in request.POST:
            payment_order = PaymentOrder.objects.get(pk=context['payment'].payment_order_id)
            payment_order.track_order_status = request.POST['track_order_status']
            payment_order.save()
            return redirect("main_admin:view-payments")
    return render(request, 'main_admin/edit_payment.html', context)


@checkLogin('admin')
def view_orders(request):
    context = {}
    context['active'] = 'orders'
    get_common_context(request, context)
    
    order_list = Order.all_objects.all().order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(order_list, 5)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context['orders'] = orders
    return render(request, 'main_admin/view_orders.html', context)

@checkLogin('admin')
def edit_about_us(request):
    context = {}
    context['active'] = 'about_us'
    get_common_context(request, context)
    context['about_us'] = AboutUs.objects.all().first()
    context['about_form'] = AboutForm(request.POST or None, request.FILES or None, instance=context['about_us'])

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            about_us_data = {
                'title': data['title'],
                'main_intro': data['main_intro'],
                'description': data['description'],
                'address': data['address'],
                'phone': data['phone'],
                'email': data['email']
            }

            if context['about_us']:
                context['about_us'] = AboutUs.objects.filter(pk=context['about_us'].pk)
                context['about_us'].update(**about_us_data)
                context['about_us'] = context['about_us'].first()
            else:
                context['about_us'] = AboutUs.objects.create(**about_us_data)

            context['about_form'] = AboutForm(request.POST or None, request.FILES or None, instance=context['about_us'])
            if context['about_form'].is_valid():
                context['about_form'].save()

            # Social Link
            new_social = { k:v for k,v in data.items() if k.startswith('new_social') }
            old_social = { k:v for k,v in data.items() if k.startswith('social_') }
            result_new = {}
            for key, value in new_social.items():
                no = key.split('_')[-1]
                field = key.split('_')[-2]
                if no not in result_new:
                    result_new[no] = {}
                result_new[no][field] = value
            
            result_old = {}
            for key, value in old_social.items():
                no = key.split('_')[-1]
                field = key.split('_')[-2]
                if no not in result_old:
                    result_old[no] = {}
                result_old[no][field] = value
            
            del result_old['id'] # remove social_link_id
            # save
            for social in context['about_us'].social_links.all():
                key = str(social.pk)
                if key in [*result_old]:
                    social.social_icon = result_old[key]['icon']
                    social.link = result_old[key]['link']
                    social.save()
                else:
                    context['about_us'].social_links.remove(social)

            for key, value in result_new.items():
                social = SocialLink.objects.create(social_icon= value['icon'], link=value['link'])
                context['about_us'].social_links.add(social)
            context['about_us'].save()
    except Exception as err:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'main_admin/edit_about_us.html', context)

@checkLogin('admin')
def edit_details(request, detail_type):
    context = {}
    context['active'] = 'faq' if detail_type is const.FAQ else 'return_policy'
    print(context['active'])
    get_common_context(request, context)
    context['detail_type'] = detail_type
    context['details'] = Details.objects.filter(detail_type=detail_type).first()
    if (request.method == 'POST'):
        context['details'].description = request.POST['description']
        context['details'].save()
    return render(request, 'main_admin/edit_details.html', context)
