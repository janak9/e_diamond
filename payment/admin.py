from django.contrib import admin
from payment.models import PaymentOrder, Payment

# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentOrder)
