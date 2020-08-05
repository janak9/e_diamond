from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from base import const
from base.utils import MyValidation
import os
import uuid

def get_image_path(instance, filename):
    return os.path.join('product', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))

def get_logo_path(instance, filename):
    return os.path.join('logo', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))

class Image(models.Model):
    class Meta:
        db_table = 'image'

    src = models.ImageField(_('image'), upload_to=get_image_path, blank=False, null=False)

    def save(self, *args, **kwargs):
        try:
            this = Image.objects.get(id=self.id)
            if this.src not in ['product/default-product.jpg', 'logo/share-default.png']:
                if this.src != self.src:
                    this.src.delete(save=False)
        except:
            pass
        super(Image, self).save(*args, **kwargs)


class SocialLink(models.Model):
    class Meta:
        db_table = 'soical_link'

    social_icon = models.CharField(_('social icon'), max_length=50, blank=False, null=False, default='fa fa-external-link')
    link = models.TextField(_('social link'), blank=False, null=False)

    def __str__(self):
        return self.link


class Contact(models.Model):
    class Meta:
        db_table = 'contact'

    contact_type = models.PositiveSmallIntegerField(choices=const.CONTACT_TYPE_CHOICES, default=const.CONTACT_US)
    name = models.CharField(_('full name'), max_length=50, blank=False, null=False, validators=[MyValidation.ALPHA_SPACE])
    email = models.CharField(_('email'), max_length=50, blank=False, null=False)
    phone = models.CharField(_('contact no'), max_length=18, blank=True, null=True, validators=[MyValidation.PHONE_NO])
    country = models.CharField(_('country'), max_length=15, blank=True, null=True)
    subject = models.CharField(_('subject'), max_length=80, blank=False, null=False)
    message = models.TextField(_('message'), blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=const.READ_STATUS_CHOICES, default=const.NOT_CHECKED)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.email, self.name)


class AboutUs(models.Model):
    class Meta:
        db_table = 'about_us'

    title = models.CharField(_('title'), max_length=200, blank=True, null=True)
    main_intro = models.TextField(_('main intro'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    address = models.TextField(_('address'), blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=18, blank=True, null=True, validators=[MyValidation.PHONE_NO])
    email = models.CharField(_('email'), max_length=50, blank=False, null=False)
    logo = models.ImageField(_('logo'), help_text=_('social media logo'), upload_to=get_logo_path, blank=False, null=False)
    social_links = models.ManyToManyField(SocialLink, related_name='about_us', blank=True)


class Details(models.Model):
    class Meta:
        db_table = 'details'

    detail_type = models.PositiveSmallIntegerField(choices=const.DETAILS_TYPE_CHOICES, default=const.FAQ)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return str(self.get_detail_type_display())

class Offer(models.Model):
    class Meta:
        db_table = 'offer'

    title = models.CharField(_('title'), max_length=150, blank=False, null=False)
    description = models.TextField(_('description'), blank=True, null=True)
    code = models.CharField(_('coupon code'), max_length=10, unique=True, blank=False, null=False)
    discount = models.FloatField(_('discount'), blank=False, null=False, default=0, validators=[MinValueValidator(0.01), MaxValueValidator(100)])
    start_time = models.DateTimeField(_('start time'), blank=False, null=False, help_text=_('offer start time'))
    end_time = models.DateTimeField(_('end time'), blank=False, null=False, help_text=_('end start time'))
    minimun_order_price = models.FloatField(_('minimum order price'), blank=True, null=True)
    maximun_discount = models.FloatField(_('maximum discount'), blank=True, null=True)
    offer_type = models.PositiveSmallIntegerField(choices=const.OFFER_TYPE_CHOICES, default=const.FLAT)
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)

    def __str__(self):
        return '{} {}'.format(self.code, self.title)