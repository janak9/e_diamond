from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from auth_user.models import User as user_model
from decouple import config
from base import const, mail
from auth_user.decorator import checkLogin
from payment.models import PaymentOrder, Payment
from product.models import Product
from user.models import Cart
import json
import traceback


@checkLogin('both')
def confirm(request, pk):
    context = {
        'app_name': config('APP_NAME'),
        'payment_order': PaymentOrder.objects.get(pk=pk)
    }
    try:
        if request.method == 'POST':
            context['payment_order'].status = const.CANCELLED
            context['payment_order'].save()
            return redirect('user:checkout')

        context['options'] = {
            "key": config('KEY_ID'),
            "amount": context['payment_order'].price,
            "currency": "INR",
            "name": context['app_name'],
            "image": request.build_absolute_uri(static('user/images/apple-touch-icon.png')),
            "order_id": context['payment_order'].razorpay_order_id,
            "callback_url": request.build_absolute_uri(reverse('payment:success', kwargs={"pk": context['payment_order'].pk})),
            "redirect": "true",
            "prefill": {
                "name": request.user.get_full_name(),
                "email": request.user.email,
                "contact": request.user.phone
            }
        }
        print(context['options'])
        return render(request, 'payment/confirm.html', context)
    except:
        traceback.print_exc()

    return HttpResponse("Something was wrong! <a href='" + reverse('user:home') + "'>Back To Home</a>")


@csrf_exempt
def success(request, pk):
    try:
        context = {'app_name': config('APP_NAME'), 'payment_order': PaymentOrder.objects.get(pk=pk)}
        if request.method == 'POST':
            data = request.POST.dict()
            print(data)
            payload = {'user_id': context['payment_order'].user_id, 'payment_order': context['payment_order'],
                       'razorpay_response': json.dumps(data), 'status': const.PAID}
            if 'error[code]' in data:
                payload['status'] = const.FAILED
            else:
                Cart.objects.filter(user_id=context['payment_order'].user_id).delete()
                for order in context['payment_order'].order.all():
                    product = Product.objects.get(pk=order.product_id)
                    product.available_qty -= order.qty
                    product.save()
            context['payment'] = Payment.objects.create(**payload)
            context['payment_order'].status = payload['status']
            context['payment_order'].save()
            print(context['payment_order'])

            if payload['status'] == const.PAID:
                user = user_model.objects.filter(user_type=const.ADMIN)
                mail.send_email(user, "order_admin", payment_order=context['payment_order'])
                mail.send_email(context['payment_order'].user, "order_user", payment_order=context['payment_order'])
                return render(request, 'payment/success.html', context)
            else:
                return redirect('payment:failure', pk=pk)

    except:
        traceback.print_exc()

    return HttpResponse("Something was wrong! <a href='" + reverse('user:home') + "'>Back To Home</a>")


def failure(request, pk):
    context = {'app_name': config('APP_NAME'), 'payment_order': PaymentOrder.objects.get(pk=pk)}
    return render(request, 'payment/failure.html', context)
