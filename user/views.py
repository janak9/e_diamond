from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from base import const
from auth_user.decorator import checkLogin
from product.models import MainCategory, Category, SubCategory, Product
from main_admin.models import Image, AboutUs, Offer, Contact
from user.models import Wishlist, Cart, Compare, Address, Order
from payment.models import PaymentOrder, Payment
from decouple import config
import sys
import json

def get_common_context(context):
    context['app_name'] = config('APP_NAME')
    context['main_categories'] = MainCategory.objects.all()
    context['categories'] = Category.objects.all()
    context['about_us'] = AboutUs.objects.all()[0]
    context['offers'] = Offer.objects.order_by("-timestamp")
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

def contact_us(request):
    context = {}
    context['active'] = 'contact_us'
    get_common_context(context)

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp)) # remove extra fields
            Contact.objects.create(**data)
            context['msg'] = "Thank You! For reaching us, will you contact soon."
    except Exception as err:
        print(err)
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'user/contact_us.html', context)

def post_requirment(request):
    context = {}
    context['active'] = 'post_requirment'
    get_common_context(context)

    try:
        if (request.method == 'POST'):
            data = request.POST.dict()
            tmp = ['csrfmiddlewaretoken']
            list(map(data.pop, tmp)) # remove extra fields
            data['contact_type'] = const.POST_REQUIRMENT
            Contact.objects.create(**data)
            context['msg'] = "Thank You! For reaching us, will you contact soon."
    except Exception as err:
        print(err)
        context['msg'] = "Oops, Something was wrong! Please try again."

    return render(request, 'user/post_requirment.html', context)

def products(request, main_category_id):
    context = {}
    context['active'] = 'products'
    get_common_context(context)
    filter_attr = {}
    filter_attr['sub_category'] = request.GET.getlist('sub_category[]')
    filter_attr['min_amount'] = request.GET.get('min_amount', 0)
    filter_attr['max_amount'] = request.GET.get('max_amount', 30000)
    filter_attr['sort_by'] = request.GET.get('sort_by')
    context['filter_attr'] = filter_attr
    context['main_category'] = MainCategory.objects.get(pk=main_category_id)

    if (filter_attr['sort_by'] != '' and filter_attr['sort_by'] == 'price_desc'):
        orderbyList = ['-price']
    elif (filter_attr['sort_by'] != '' and filter_attr['sort_by'] == 'price_asc'):
        orderbyList = ['price']
    else:
        orderbyList = ['-timestamp']
    
    if (len(filter_attr['sub_category']) > 0):
        products_list = Product.objects.filter(main_category__pk=main_category_id, sub_category__pk__in=filter_attr['sub_category'], price__range=(filter_attr['min_amount'], filter_attr['max_amount'])).order_by(*orderbyList)
    else:
        products_list = Product.objects.filter(main_category__pk=main_category_id, price__range=(filter_attr['min_amount'], filter_attr['max_amount'])).order_by(*orderbyList)

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
    context = {}
    context['active'] = 'products'
    get_common_context(context)
    context['product'] = Product.objects.get(pk=pk)
    return render(request, 'user/product_details.html', context)

@checkLogin('both')
def wishlist(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
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
        if (wishlist.count() > 0):
            result['status'] = 'success'
            result['msg'] = 'already added in wishlist'
        else:
            Wishlist.objects.create(user_id=user_id, product_id=product_id)
            result['status'] = 'success'
            result['msg'] = 'successfully added to wishlist'
    except Exception as err:
        print(err)
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))

@checkLogin('both')
def remove_wishlist(request, pk):
    wishlist = Wishlist.objects.get(id=pk)
    wishlist.delete()
    return redirect("user:wishlist")

@checkLogin('both')
def cart(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['cart_bill'] = calculate_bill({ 'user_id': request.user.id })
    context['carts'] = Cart.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/cart.html', context)

@csrf_exempt
@checkLogin('both')
def add_cart(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        product_id = data['product_id']
        qty = data['qty']
        user_id = request.user.id
        cart = Cart.objects.filter(user_id=user_id, product_id=product_id)
        if (cart.count() > 0):
            if (cart[0].qty != qty):
                cart[0].qty = qty
                cart[0].save()
                result['status'] = 'updated'
                result['msg'] = 'cart successfully updated'
        else:
            Cart.objects.create(user_id=user_id, product_id=product_id, qty=qty)
        result['status'] = 'success'
        result['msg'] = 'successfully added to cart'
    except Exception as err:
        print(err)
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))

@csrf_exempt
@checkLogin('both')
def update_cart(request):
    result = {}
    try:
        data = json.loads(request.POST.get('data'))
        product_id = data['product_id']
        qty = data['qty']
        coupon_code = data['coupon_code']
        user_id = request.user.id
        cart = Cart.objects.filter(user_id=user_id, product_id=product_id)
        if (cart.count() <= 0):
            result['status'] = 'error'
            result['msg'] = 'product not found in cart!'
            return HttpResponse(json.dumps(result))
        else:
            cart = cart.get()
            if (cart.qty != qty):
                cart.qty = qty
                cart.save()
            result['cart_bill'] = calculate_bill({ 'user_id': user_id, 'coupon_code': coupon_code })
            result['status'] = 'success'
            result['msg'] = 'cart successfully updated'
    except Exception as err:
        print('update_cart - ', err)
        result['status'] = 'error'
        result['msg'] = 'something is wrong!'

    return HttpResponse(json.dumps(result))

@checkLogin('both')
def remove_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return redirect("user:cart")

def calculate_bill(input):
    try:
        result = {}
        carts = Cart.objects.filter(user_id=input['user_id']).all()
        result['tax'] = 0
        result['shipping_cost'] = 0
        result['sub_total'] = 0
        result['coupon_discount'] = 0
        for cart in carts:
            result['sub_total'] += (cart.qty * cart.product.price)
        
        # TODO : check coupon
        result['grand_total'] = result['sub_total'] - result['coupon_discount'] + result['tax']
        return result
    except Exception as err:
        print('calculate_bill - ', err)
        raise err

@checkLogin('both')
def checkout(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['billing_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.BILLING)
    context['shipping_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.SHIPPING)
    context['cart_bill'] = calculate_bill({ 'user_id': request.user.id })
    context['carts'] = Cart.objects.filter(user_id=request.user.id).order_by('-timestamp')
    try:
        if (request.method == 'POST'):
            user_id = request.user.id
            payment_data = {}
            payment_data['user_id'] = user_id
            payment_data['price'] = context['cart_bill']['grand_total']
            payment_data['bill'] = json.dumps(context['cart_bill'])
            payment_order = PaymentOrder(**payment_data)
            payment_order.save()

            receipt = str(config('RECEIPT_PREFIX')) + '_' + str(payment_order.pk)
            payment_order.receipt = receipt

            # create razorpay_order
            razorpay_order_payload = {}
            razorpay_order_payload['amount'] = int(payment_data['price']) * 100 # razorpay accept money in 'paisa' so need to convert ruppes to paisa
            razorpay_order_payload['currency'] = 'INR'
            razorpay_order_payload['receipt'] = receipt
            razorpay_order_payload['notes'] = {'user_id': user_id, **context['cart_bill']}
            razorpay_order_payload['payment_capture'] = '1'
            print(razorpay_order_payload)
            razorpay_order = settings.RAZORPAY.order.create(razorpay_order_payload)
            print(razorpay_order)
            payment_order.razorpay_order_response = json.dumps(razorpay_order)
            payment_order.razorpay_order_id = razorpay_order['id']
            payment_order.save()

            for cart in context['carts']:
                data = {}
                data['user_id'] = user_id
                data['product_id'] = cart.product.pk
                data['qty'] = cart.qty
                data['price'] = cart.product.price
                order = Order.objects.create(**data)
                payment_order.order.add(order)
                payment_order.save()
            return redirect('payment:confirm', pk=payment_order.pk)
    except Exception as err:
        print(err)
        context['msg'] = "Sorry for the inconvenience, Something was wrong! please try again or contact customer support."
    return render(request, 'user/checkout.html', context)

@checkLogin('both')
def my_account(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    return render(request, 'user/my_account.html', context)

@checkLogin('both')
def login_security(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    return render(request, 'user/login_security.html', context)

@checkLogin('both')
def offers(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['offers'] = Offer.objects.all()
    return render(request, 'user/offers.html', context)

@checkLogin('both')
def address(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['billing_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.BILLING)
    context['shipping_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.SHIPPING)

    if (request.method == 'POST'):
        data = request.POST.dict()
        tmp = ['csrfmiddlewaretoken']
        if 'same_address' in data:
            del data['same_address']
        list(map(data.pop, tmp)) # remove extra fields
        billing = {k.replace('billing_', ''): v for k, v in data.items() if k.startswith('billing')}
        shipping = {k.replace('shipping_', ''): v for k, v in data.items() if k.startswith('shipping')}
        if (context['billing_address'].count() <= 0):
            billing['user_id'] = request.user.id
            billing['address_type'] = const.BILLING
            address = Address.objects.create(**billing)
        else:
            context['billing_address'].update(**billing)

        if (context['shipping_address'].count() <= 0):
            shipping['user_id'] = request.user.id
            shipping['address_type'] = const.SHIPPING
            context['shipping_address'] = Address.objects.create(**shipping)
        else:
            context['shipping_address'].update(**shipping)
    
    return render(request, 'user/address.html', context)

@checkLogin('both')
def orders(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['orders'] = Order.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/orders.html', context)

@checkLogin('both')
def payments(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['payments'] = PaymentOrder.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/payments.html', context)

@checkLogin('both')
def invoice(request, pk):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['payment'] = Payment.objects.get(pk=pk)
    context['bill'] = json.loads(context['payment'].payment_order.bill)
    context['billing_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.BILLING)
    context['shipping_address'] = Address.objects.filter(user_id=request.user.id, address_type=const.SHIPPING)
    return render(request, 'user/invoice.html', context)
