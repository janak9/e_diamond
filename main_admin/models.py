from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_image_path(instance, filename):
    return os.path.join('product', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))

def get_logo_path(instance, filename):
    return os.path.join('logo', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))

class Image(models.Model):
    class Meta:
        db_table = 'image'

    title = models.CharField(_('title'), max_length=80, blank=False, null=False)
    src = models.ImageField(_('image'), upload_to=get_image_path, blank=False, null=False)


class SocialType(models.Model):
    class Meta:
        db_table = 'social_type'

    name = models.CharField(max_length=20, help_text=_('Social Media Name'), blank=False, null=False)
    logo = models.ImageField(_('logo'), help_text=_('social media logo'), upload_to=get_logo_path, blank=False, null=False)


class SocialLink(models.Model):
    class Meta:
        db_table = 'soical_link'

    social_type = models.ForeignKey(SocialType, on_delete=models.SET_DEFAULT, default='logo/share-default.png', blank=False)
    link = models.TextField(_('social link'), blank=False, null=False)

