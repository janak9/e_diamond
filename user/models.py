from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from base.utils import MyValidation
from base import const, managers
from product.models import Product
from main_admin.models import Offer


class Address(models.Model):
    class Meta:
        db_table = 'address'

    user = models.ForeignKey(get_user_model(), related_name="address", on_delete=models.CASCADE, blank=False, null=False)
    address_type = models.CharField(max_length=10, default=const.BILLING, choices=const.ADDRESS_TYPE, blank=False, null=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, validators=[MyValidation.ALPHA])
    last_name = models.CharField(_('last name'), max_length=30, blank=True, validators=[MyValidation.ALPHA])
    company_name = models.CharField(_('company name'), max_length=50, blank=True, null=True)
    appartment = models.CharField(_('appartment'), max_length=20, blank=False, null=False)
    street_address = models.CharField(_('street address'), max_length=150, blank=False, null=False)
    city = models.CharField(_('city'), max_length=20, blank=False, null=False, validators=[MyValidation.ALPHA])
    country = models.CharField(_('country'), max_length=20, blank=False, null=False, validators=[MyValidation.ALPHA])
    pin_code = models.CharField(_('pin code'), max_length=6, blank=False, null=False, validators=[MyValidation.NUM])


class Feedback(models.Model):
    class Meta:
        db_table = 'feedback'

    user = models.ForeignKey(get_user_model(), related_name="feedback", on_delete=models.CASCADE, blank=False, null=False)
    star = models.FloatField(_('star'), blank=False, null=False, default=1.0, validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
    comment = models.CharField(_('comment'), max_length=250, blank=False, null=False)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)
    read_status = models.PositiveSmallIntegerField(choices=const.READ_STATUS_CHOICES, default=const.NOT_CHECKED)

    objects = managers.StatusManager()
    all_objects = managers.StatusManager(active_only=False)


class Compare(models.Model):
    class Meta:
        db_table = 'compare'

    user = models.ForeignKey(get_user_model(), related_name="compare", on_delete=models.CASCADE, blank=False, null=False)
    product = models.ManyToManyField(Product, related_name="compare", blank=True)


class Wishlist(models.Model):
    class Meta:
        db_table = 'wishlist'

    user = models.ForeignKey(get_user_model(), related_name="wishlist", on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, related_name="wishlist", on_delete=models.CASCADE, blank=False, null=False)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)


class Cart(models.Model):
    class Meta:
        db_table = 'cart'

    user = models.ForeignKey(get_user_model(), related_name="cart", on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, related_name="cart", on_delete=models.CASCADE, blank=False, null=False)
    qty = models.FloatField(_('quantity'), blank=False, null=False)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)


class Order(models.Model):
    class Meta:
        db_table = 'order'

    user = models.ForeignKey(get_user_model(), related_name="order", on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, related_name="order", on_delete=models.DO_NOTHING, blank=False, null=False)
    qty = models.FloatField(_('quantity'), blank=False, null=False)
    price = models.FloatField(_('price'), help_text='price per quantity', blank=False, null=False)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)

    objects = managers.StatusManager()
    all_objects = managers.StatusManager(active_only=False)
