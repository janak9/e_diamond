from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from base.utils import MyValidation
from base import const
from django.core.validators import FileExtensionValidator
import os
import uuid


def get_profile_path(instance, filename):
    return os.path.join('profile', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('user_type', const.ADMIN)
        extra_fields.setdefault('last_name', "admin")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "user"

    email = models.EmailField(unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False, null=False, validators=[MyValidation.ALPHA])
    last_name = models.CharField(_('last name'), max_length=30, blank=False, null=False, validators=[MyValidation.ALPHA])
    user_type = models.PositiveSmallIntegerField(choices=const.USER_TYPE_CHOICES, default=const.USER, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this user should be treated as active.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    phone = models.CharField(_('contact no'), max_length=18, blank=True, null=True, validators=[MyValidation.PHONE_NO])
    gender = models.CharField(max_length=6, default=const.MALE, choices=const.GENDER_TYPE, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=get_profile_path, help_text='profile photo', blank=True, default='profile/user-square.jpeg')
    status = models.PositiveSmallIntegerField(choices=const.STATUS_CHOICES, default=const.ACTIVE)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return "{} {}.".format(self.first_name, self.last_name[0])

    def get_username(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            this = User.objects.get(id=self.id)
            if this.profile_pic != 'profile/user-square.jpeg':
                if this.profile_pic != self.profile_pic:
                    this.profile_pic.delete(save=False)
        except:
            pass
        super(User, self).save(*args, **kwargs)
