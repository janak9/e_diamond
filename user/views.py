from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from auth_user.decorator import checkLogin
from product.models import MainCategory, Category, SubCategory, Product
from main_admin.models import Image, AboutUs, Offer
from user.models import Wishlist, Cart, Compare

def get_common_context(context):
    context['test'] = 'test'
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
    return render(request, 'user/contact_us.html', context)

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

    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 20)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context['products'] = products
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

@checkLogin('both')
def cart(request):
    context = {}
    context['active'] = 'my_account'
    get_common_context(context)
    context['carts'] = Cart.objects.filter(user_id=request.user.id).order_by('-timestamp')
    return render(request, 'user/cart.html', context)
