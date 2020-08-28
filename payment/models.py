from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from base import const
from user.models import Order
from main_admin.models import Offer

class PaymentOrder(models.Model):
    class Meta:
        db_table = 'payment_order'

    user = models.ForeignKey(get_user_model(), related_name="payment_order", on_delete=models.CASCADE, blank=False, null=False)
    order = models.ManyToManyField(Order, related_name="payment_order", blank=False)
    price = models.FloatField(_('payable price'), blank=False, null=False)
    offer = models.ForeignKey(Offer, related_name="payment_order", on_delete=models.DO_NOTHING, blank=True, null=True)
    bill = models.TextField(_('bill calculation'), blank=False, null=False)
    razorpay_order_id = models.CharField(_('razorpay order id'), max_length=150, blank=False, null=True)
    razorpay_order_response = models.TextField(_('razorpay order response'), blank=False, null=True)
    receipt = models.CharField(_('receipt'), max_length=150, blank=False, null=True)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=const.PAYMENT_STATUS_CHOICES, default=const.PENDING)
    track_order_status = models.PositiveSmallIntegerField(choices=const.TRACK_ORDER_STATUS_CHOICES, default=const.PENDING)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.user.get_full_name(), self.get_status_display(), self.receipt, self.razorpay_order_id)

class Payment(models.Model):
    class Meta:
        db_table = 'payment'

    user = models.ForeignKey(get_user_model(), related_name="payment", on_delete=models.CASCADE, blank=False, null=False)
    payment_order = models.ForeignKey(PaymentOrder, related_name="payment", on_delete=models.DO_NOTHING, blank=False, null=False)
    razorpay_response = models.TextField(_('razorpay response'), blank=False, null=False)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=const.PAYMENT_STATUS_CHOICES, default=const.PENDING)

    def __str__(self):
        return "{} - {}".format(self.user.get_full_name(), self.get_status_display())
