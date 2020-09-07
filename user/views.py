from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.timezone import get_current_timezone
from django.urls import reverse
from auth_user.models import User as user_model
from auth_user.decorator import checkLogin
from base import const, mail
from product.models import MainCategory, Category, Product, Review
from main_admin.models import AboutUs, Offer, Contact, Details
from user.models import Wishlist, Cart, Compare, Address, Order, Feedback
from payment.models import PaymentOrder, Payment
from decouple import config
import json
import traceback
from datetime import datetime


def get_common_context(request, context):
    context['app_name'] = config('APP_NAME')
    context['main_categories'] = MainCategory.objects.all()
    context['categories'] = Category.objects.all()
    context['about_us'] = AboutUs.objects.all()[0]
    context['offers'] = Offer.objects.order_by("-timestamp")
    try:
        if request.user.is_authenticated:
            context['compare_products'] = Compare.objects.filter(user_id=request.user.id).first().product.all()
    except:
        traceback.print_exc()
    context['top_10_products'] = Product.objects.order_by("-timestamp")[:10]


def home(request):
    context = {'active': 'home'}
    get_common_context(request, context)
    return render(request, 'user/index.html', context)


def about(request):
    context = {'active': 'about'}
    get_common_context(request, context)
    return render(request, 'user/about.html', context)


def faq(request):
    context = {}
    get_common_context(request, context)
    context['faq'] = Details.objects.filter(detail_type=const.FAQ).first()
    return render(request, 'user/faq.html', context)


def return_policy(request):
    context = {}
    get_common_context(request, context)
    context['return_policy'] = Details.objects.filter(detail_type=const.RETURN_POLICY).first()
    return render(request, 'user/return_policy.html', context)


def contact_us(request):
    context = {'active': 'contact_us'}
    get_common_context(request, context)

    try:
        if request.method == 'POST':
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp))  # remove extra fields
            contact = Contact.objects.create(**data)
            user = user_model.objects.filter(user_type=const.ADMIN)
            mail.send_email(user, "contact", contact=contact)
            context['msg'] = "Thank You! For reaching us, we will you contact soon."
    except:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'user/contact_us.html', context)


def post_requirement(request):
    context = {'active': 'post_requirement'}
    get_common_context(request, context)

    try:
        if request.method == 'POST':
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp))  # remove extra fields
            data['contact_type'] = const.POST_REQUIREMENT
            contact = Contact.objects.create(**data)
            user = user_model.objects.filter(user_type=const.ADMIN)
            mail.send_email(user, "contact", contact=contact)
            context['msg'] = "Thank You! For reaching us, we will you contact soon."
    except:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'user/post_requirement.html', context)


@checkLogin('both')
def feedback(request):
    context = {'active': 'feedback'}
    get_common_context(request, context)

    try:
        if request.method == 'POST':
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp))  # remove extra fields
            data['user_id'] = request.user.pk
            Feedback.objects.create(**data)
            context['msg'] = "Thank You! For Giving Feedback to us."
    except:
        traceback.print_exc()
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'user/feedback.html', context)


# product
def products(request, main_category_id):
    context = {'active': 'products'}
    get_common_context(request, context)
    filter_attr = {'sub_category': request.GET.getlist('sub_category[]'),
                   'min_amount': request.GET.get('min_amount', 0),
                   'max_amount': request.GET.get('max_amount', 30000),
                   'sort_by': request.GET.get('sort_by')}
    context['filter_attr'] = filter_attr
    context['main_category'] = MainCategory.objects.get(pk=main_category_id)

    if filter_attr['sort_by'] != '' and filter_attr['sort_by'] == 'price_desc':
        order_list = ['-price']
    elif filter_attr['sort_by'] != '' and filter_attr['sort_by'] == 'price_asc':
        order_list = ['price']
    else:
        order_list = ['-timestamp']

    if len(filter_attr['sub_category']) > 0:
        products_list = Product.objects.filter(
            main_category__pk=main_category_id,
            sub_category__pk__in=filter_attr['sub_category'],
            price__range=(filter_attr['min_amount'], filter_attr['max_amount'])
        ) \
            .order_by(*order_list)
    else:
        products_list = Product.objects.filter(
            main_category__pk=main_category_id,
            price__range=(filter_attr['min_amount'], filter_attr['max_amount'])
        ) \
            .order_by(*order_list)

    # page = request.GET.get('page', 1)
    # paginator = Paginator(products_list, 20)
    # try:
    #     products = paginator.page(page)
    # except PageNotAnInteger:
    #     products = paginator.page(1)
    # except EmptyPage:
    #     products = paginator.page(paginator.num_pages)
    context['products'] = products_list
    return render(request, 'user/products.html', context)


def product_details(request, pk):
    context = {'active': 'products'}
    get_common_context(request, context)
    context['product'] = Product.objects.get(pk=pk)
    context['reviews'] = Review.objects.filter(product_id=pk).order_by('-timestamp')
    return render(request, 'user/product_details.html', context)


def description(request, pk):
    product = Product.objects.get(pk=pk)
    res = render(request, 'user/description.html', {'product': product})
    res['X-Frame-Options'] = 'SAMEORIGIN'
    return res


def search_diamond(request):
    context = {'active': 'search_diamond', 'CONST': const}
    get_common_context(request, context)
    filter_attr = {
        'min_size': request.GET.get('min_size', 0.01),
        'max_size': request.GET.get('max_size', 10),
        'min_diameter': request.GET.get('min_diameter', 0.01),
        'max_diameter': request.GET.get('max_diameter', 12),
        'shape': request.GET.getlist('shape[]'),
        'cut': request.GET.getlist('cut[]'),
        'symmetry_cut': request.GET.getlist('symmetry_cut[]'),
        'purity': request.GET.getlist('purity[]'),
        'color': request.GET.getlist('color[]'),
        'fluorescence': request.GET.getlist('fluorescence[]'),
    }
    context['filter_attr'] = filter_attr

    filter_conditions = {
        'polish__isnull': False,
        'polish__size__range': (filter_attr['min_size'], filter_attr['max_size']),
        'polish__diameter__range': (filter_attr['min_diameter'], filter_attr['max_diameter'])
    }

    if len(filter_attr['shape']) > 0:        filter_conditions['polish__shape__in'] = filter_attr['shape']
    if len(filter_attr['cut']) > 0:          filter_conditions['polish__cut__in'] = filter_attr['cut']
    if len(filter_attr['symmetry_cut']) > 0: filter_conditions['polish__symmetry_cut__in'] = filter_attr['symmetry_cut']
    if len(filter_attr['purity']) > 0:       filter_conditions['polish__purity__in'] = filter_attr['purity']
    if len(filter_attr['color']) > 0:        filter_conditions['polish__color__in'] = filter_attr['color']
    if len(filter_attr['fluorescence']) > 0: filter_conditions['polish__fluorescence__in'] = filter_attr['fluorescence']

    print(filter_conditions)
    context['products'] = Product.objects.filter(**filter_conditions)
    return render(request, 'user/search_diamond.html', context)


@csrf_exempt
@checkLogin('both')
def add_review(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        product_id = data['product_id']
        comment = data['comment']
        star = data['star']
        user_id = request.user.id
        product = PaymentOrder.objects.filter(user_id=user_id, status=const.PAID, order__product_id=product_id)
        if product.count() > 0:
            Review.objects.create(user_id=user_id, product_id=product_id, star=star, comment=comment)
            result['status'] = 'success'
        else:
            result['status'] = 'not_buy'
            result['msg'] = "you haven't buy this product. so, you can't give review."
    except:
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))


# wishlist
@checkLogin('both')
def wishlist(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['wishlists'] = Wishlist.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/wishlist.html', context)


@csrf_exempt
@checkLogin('both')
def add_wishlist(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        product_id = data['product_id']
        user_id = request.user.id
        wishlist = Wishlist.objects.filter(user_id=user_id, product_id=product_id)
        if wishlist.count() > 0:
            result['status'] = 'success'
            result['msg'] = 'already added in wishlist'
        else:
            Wishlist.objects.create(user_id=user_id, product_id=product_id)
            result['status'] = 'success'
            result['msg'] = 'successfully added to wishlist'
    except:
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))


@checkLogin('both')
def remove_wishlist(request, pk):
    wishlist = Wishlist.objects.get(id=pk)
    wishlist.delete()
    return redirect("user:wishlist")


# cart
@checkLogin('both')
def cart(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    today = datetime.now(tz=get_current_timezone())
    context['offers'] = Offer.objects.filter(end_time__gte=today)
    context['cart_bill'] = calculate_bill(request)
    context['carts'] = Cart.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/cart.html', context)


@csrf_exempt
@checkLogin('both')
def add_cart(request, product_id):
    try:
        user_id = request.user.id
        cart = Cart.objects.filter(user_id=user_id, product_id=product_id)
        if cart.count() <= 0:
            Cart.objects.create(user_id=user_id, product_id=product_id, qty=1)
    except Exception as err:
        print('update_cart - ', err)
        traceback.print_exc()
    return redirect("user:cart")


@csrf_exempt
@checkLogin('both')
def update_cart(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        product_id = data['product_id']
        qty = data['qty']
        user_id = request.user.id
        cart = Cart.objects.filter(user_id=user_id, product_id=product_id)
        if cart.count() <= 0:
            result['status'] = 'error'
            result['msg'] = 'product not found in cart!'
            return HttpResponse(json.dumps(result))
        else:
            cart = cart.get()
            if cart.qty != qty:
                cart.qty = qty
                cart.save()
            result['cart_bill'] = calculate_bill(request)
            result['status'] = 'success'
            result['msg'] = 'cart successfully updated'
    except Exception as err:
        print('update_cart - ', err)
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))


@checkLogin('both')
def remove_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return redirect("user:cart")


@csrf_exempt
@checkLogin('both')
def verify_offer(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        coupon_code = data['coupon_code']
        request.session['coupon_code'] = coupon_code
        result['cart_bill'] = calculate_bill(request)
        result['status'] = 'success'
        del request.session['coupon_code']
    except:
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    hr = HttpResponse(json.dumps(result))
    hr.set_signed_cookie('coupon_code', coupon_code, max_age=60*60*24)
    return hr


def calculate_bill(request):
    try:
        result = {}
        user_id = request.user.id
        carts = Cart.objects.filter(user_id=user_id).all()
        result['tax'] = 0
        result['shipping_cost'] = 0
        result['sub_total'] = 0
        result['coupon_discount'] = 0
        for cart in carts:
            result['sub_total'] += (cart.qty * cart.product.price)

        offer_response = check_offer(request)
        if offer_response:
            result['offer_response'] = offer_response
            if offer_response['status'] == 'success':
                offer = offer_response['offer']
                offer_response['offer_id'] = offer.pk
                offer_response['offer_title'] = offer.title
                offer_response['offer_code'] = offer.code
                del offer_response['offer']
                if result['sub_total'] < offer.minimun_order_price:
                    offer_response['status'] = 'error'
                    offer_response['msg'] = 'The order price is below the minimum price for the applied offer!'
                else:
                    if offer.offer_type == const.PERCENTAGE:
                        result['coupon_discount'] = (result['sub_total'] * offer.discount / 100)
                        if result['coupon_discount'] > offer.maximun_discount:
                            result['coupon_discount'] = offer.maximun_discount
                    elif offer.offer_type == const.FLAT:
                        result['coupon_discount'] = offer.discount

        result['grand_total'] = result['sub_total'] - result['coupon_discount'] + result['tax']
        return result
    except Exception as err:
        print('calculate_bill - ', err)
        raise err


def check_offer(request):
    result = {}
    user_id = request.user.id
    coupon_code = request.session['coupon_code'] if 'coupon_code' in request.session else None
    print(coupon_code)
    if not coupon_code: coupon_code = request.get_signed_cookie('coupon_code', None, max_age=60*60*24)
    if not coupon_code:
        return

    offer = Offer.objects.filter(code=coupon_code).first()
    if offer is None:
        result['status'] = 'error'
        result['msg'] = 'Invalid coupon code!'
        return result

    today = datetime.now(tz=get_current_timezone())
    if not (offer.start_time <= today <= offer.end_time):
        result['status'] = 'error'
        result['msg'] = 'Offer not started yet or expired!'
        return result

    is_offer_used = PaymentOrder.objects.filter(user_id=user_id, offer_id=offer.pk)\
        .exclude(status__in=[const.FAILED, const.CANCELLED])\
        .first()
    if is_offer_used:
        result['status'] = 'error'
        result['msg'] = 'You have already used coupon code once!'
        return result

    result['status'] = 'success'
    result['offer'] = offer
    return result


# compare
@checkLogin('both')
def compare(request):
    context = {}
    get_common_context(request, context)
    context['products'] = Compare.objects.filter(user_id=request.user.id).first().product.all()
    return render(request, 'user/compare.html', context)


@csrf_exempt
@checkLogin('both')
def add_compare(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        product_id = data['product_id']
        compare = Compare.objects.filter(user_id=request.user.id).first()
        if compare is None:
            compare = Compare.objects.create(user_id=request.user.id)
            compare.save()

        product = Product.objects.get(pk=product_id)
        if product not in compare.product.all():
            compare.product.add(product)
            compare.save()

        compare_products = Compare.objects.filter(user_id=request.user.id).first().product.all()
        result['compare_products_count'] = len(compare_products)
        result['compare_products_list'] = ''
        for product in compare_products:
            result['compare_products_list'] = result['compare_products_list'] + "<li>" +\
                "<a href='" + reverse('user:product-details', args=[product.pk]) + "' class='photo'><img src='" + product.images.first().src.url + "' class='cart-thumb' alt='" + product.title + "' /></a>" +\
                "<h6><a href='" + reverse('user:product-details', args=[product.pk]) + "'>" + product.title + "</a></h6>" +\
                "<p>1x - <span class='price'><i class='fas fa-rupee-sign'></i> " + str(product.price) + "</span></p>" +\
                "</li>"
        result['compare_products_list'] = result['compare_products_list'] + "<li>" +\
            "<a href='" + reverse('user:compare') + "' class='btn btn-info'>Detail View</a>" +\
            "</li>"
        result['status'] = 'success'
        result['msg'] = 'Added in compare list'
    except:
        traceback.print_exc()
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))


@checkLogin('both')
def remove_compare(request, product_id):
    try:
        compare = Compare.objects.filter(user_id=request.user.id).first()
        if compare is not None:
            product = Product.objects.get(pk=product_id)
            compare.product.remove(product)
            compare.save()
    except:
        traceback.print_exc()

    return redirect('user:compare')


# my account
@checkLogin('both')
def checkout(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['billing_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.BILLING)
    context['shipping_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.SHIPPING)
    context['cart_bill'] = calculate_bill(request)
    context['carts'] = Cart.objects.filter(user_id=request.user.id).order_by('-timestamp')
    try:
        if request.method == 'POST':
            user_id = request.user.id
            payment_data = {'user_id': user_id, 'price': context['cart_bill']['grand_total']}
            if context['cart_bill']['offer_response']:
                if context['cart_bill']['offer_response']['status'] == 'success':
                    context['cart_bill']['offer_id'] = context['cart_bill']['offer_response']['offer_id']
                    context['cart_bill']['offer_code'] = context['cart_bill']['offer_response']['offer_code']
                    payment_data['offer_id'] = context['cart_bill']['offer_response']['offer_id']
                del context['cart_bill']['offer_response']

            payment_data['bill'] = json.dumps({
                'from_address': {
                    'address': context['about_us'].address,
                    'phone': context['about_us'].phone,
                    'email': context['about_us'].email
                },
                'billing_address': context['billing_address'].values()[0],
                'shipping_address': context['shipping_address'].values()[0],
                'price': context['cart_bill']
            })
            payment_order = PaymentOrder(**payment_data)
            payment_order.save()

            receipt = str(config('RECEIPT_PREFIX')) + '_' + str(payment_order.pk)
            payment_order.receipt = receipt

            # create razorpay_order
            razorpay_order_payload = {
                'amount': int(payment_data['price']) * 100,
                'currency': 'INR',
                'receipt': receipt,
                'notes': {'user_id': user_id, **context['cart_bill']},
                'payment_capture': '1'
            }
            print(razorpay_order_payload)
            razorpay_order = settings.RAZORPAY.order.create(razorpay_order_payload)
            print(razorpay_order)
            payment_order.razorpay_order_response = json.dumps(razorpay_order)
            payment_order.razorpay_order_id = razorpay_order['id']
            payment_order.save()

            for cart in context['carts']:
                data = {'user_id': user_id, 'product_id': cart.product.pk, 'qty': cart.qty, 'price': cart.product.price}
                order = Order.objects.create(**data)
                payment_order.order.add(order)
                payment_order.save()
            return redirect('payment:confirm', pk=payment_order.pk)
    except:
        traceback.print_exc()
        context['msg'] = "Sorry for the inconvenience, Something was wrong! please try again or contact customer support."
    return render(request, 'user/checkout.html', context)


@checkLogin('both')
def my_account(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    return render(request, 'user/my_account.html', context)


@checkLogin('both')
def login_security(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    return render(request, 'user/login_security.html', context)


@checkLogin('both')
def offers(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    today = datetime.now(tz=get_current_timezone())
    context['offers'] = Offer.objects.filter(end_time__gte=today)
    return render(request, 'user/offers.html', context)


@checkLogin('both')
def address(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['billing_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.BILLING)
    context['shipping_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.SHIPPING)

    if request.method == 'POST':
        data = request.POST.dict()
        tmp = ['csrfmiddlewaretoken']
        if 'same_address' in data:
            del data['same_address']
        list(map(data.pop, tmp))  # remove extra fields
        billing = {k.replace('billing_', ''): v for k, v in data.items() if k.startswith('billing')}
        shipping = {k.replace('shipping_', ''): v for k, v in data.items() if k.startswith('shipping')}
        if context['billing_address'].count() <= 0:
            billing['user_id'] = request.user.id
            billing['address_type'] = const.BILLING
            Address.objects.create(**billing)
        else:
            context['billing_address'].update(**billing)

        if context['shipping_address'].count() <= 0:
            shipping['user_id'] = request.user.id
            shipping['address_type'] = const.SHIPPING
            context['shipping_address'] = Address.objects.create(**shipping)
        else:
            context['shipping_address'].update(**shipping)

    return render(request, 'user/address.html', context)


@checkLogin('both')
def orders(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['orders'] = Order.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/orders.html', context)


@checkLogin('both')
def payments(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['payments'] = PaymentOrder.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/payments.html', context)


@checkLogin('both')
def invoice(request, pk):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['payment'] = Payment.objects.get(pk=pk)
    bill_details = json.loads(context['payment'].payment_order.bill)
    context['billing_address'] = bill_details.get('billing_address')
    context['shipping_address'] = bill_details.get('shipping_address')
    context['from_address'] = bill_details.get('from_address')
    context['bill'] = bill_details.get('price')
    # pdf_file = Render.render_to_file('user/invoice.html', context)
    # print(pdf_file)
    return render(request, 'user/invoice.html', context)
