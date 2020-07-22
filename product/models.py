import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from base import const
from main_admin.models import Image, SocialLink

class MainCategory(models.Model):
    class Meta:
        db_table = 'main_category'

    name = models.CharField(_('name'), max_length=30, blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        db_table = 'category'

    main_category = models.ForeignKey(MainCategory, related_name='category', on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(_('name'), max_length=30, blank=False, null=False)
    image = models.ForeignKey(Image, related_name='category', on_delete=models.SET_NULL, blank=False, null=True)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        db_table = 'sub_category'

    main_category = models.ForeignKey(MainCategory, related_name='sub_category', on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey(Category, related_name='sub_category', on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)
    image = models.ForeignKey(Image, related_name='sub_category', on_delete=models.SET_NULL, blank=False, null=True)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)

    def __str__(self):
        return self.name


class AdditionalInformation(models.Model):
    class Meta:
        db_table = 'additional_information'

    title = models.CharField(_('title'), max_length=20, blank=False, null=False)
    description = models.TextField(_('description'), blank=False, null=False)

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        db_table = 'product'

    main_category = models.ForeignKey(MainCategory, related_name='product', on_delete=models.CASCADE, blank=False, null=False)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, blank=False, null=False)
    sub_category = models.ForeignKey(SubCategory, related_name='product', on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(_('title'), max_length=50, blank=False, null=False)
    description = models.TextField(_('description'), blank=False, null=False)
    qty = models.FloatField(_('quantity'), blank=False, null=False)
    available_qty = models.FloatField(_('available quantity'), blank=False, null=False)
    price = models.FloatField(_('price'), blank=False, null=False)
    images = models.ManyToManyField(Image, related_name='product', blank=True)
    social_links = models.ManyToManyField(SocialLink, related_name='product', blank=True)
    additional_information = models.ManyToManyField(AdditionalInformation, related_name='product', blank=True)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)

    def __str__(self):
        return self.title


class Review(models.Model):
    class Meta:
        db_table = 'review'

    user = models.ForeignKey(get_user_model(), related_name="review", on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, related_name="review", on_delete=models.CASCADE, blank=False, null=False)
    star = models.FloatField(_('star'), blank=False, null=False, default=1.0, validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
    comment = models.CharField(_('comment'), max_length=250, blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
