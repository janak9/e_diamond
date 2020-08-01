from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from decouple import config
from base import const
from auth_user.decorator import checkLogin
from payment.models import PaymentOrder, Payment
from user.models import Cart
import json

@checkLogin('both')
def confirm(request, pk):
    context = {}
    context['app_name'] = config('APP_NAME')
    context['payment_order'] = PaymentOrder.objects.get(pk=pk)
    try:
        if (request.method == 'POST'):
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
    except Exception as err:
        print(err)

    return HttpResponse("Something was wrong! <a href='" + reverse('user:home') + "'>Back To Home</a>")

@csrf_exempt
def success(request, pk):
    try:
        context = {}
        context['app_name'] = config('APP_NAME')
        context['payment_order'] = PaymentOrder.objects.get(pk=pk)
        if (request.method == 'POST'):
            data = request.POST.dict()
            print(data)
            payload = {}
            payload['user_id'] = context['payment_order'].user_id
            payload['payment_order'] = context['payment_order']
            payload['razorpay_response'] = json.dumps(data)
            payload['status'] = const.PAID
            if 'error[code]' in data:
                payload['status'] = const.FAILED
            else:
                Cart.objects.filter(user_id=context['payment_order'].user_id).delete()
            context['payment'] = Payment.objects.create(**payload)
            context['payment_order'].status = payload['status']
            context['payment_order'].save()
            print(context['payment_order'])

            if payload['status'] == const.PAID:
                return render(request, 'payment/success.html', context)
            else:
                return redirect('payment:failure', pk=pk)

    except Exception as err:
        print(err)

    return HttpResponse("Something was wrong! <a href='" + reverse('user:home') + "'>Back To Home</a>")

def failure(request, pk):
    context = {}
    context['app_name'] = config('APP_NAME')
    context['payment_order'] = PaymentOrder.objects.get(pk=pk)
    return render(request, 'payment/failure.html', context)
