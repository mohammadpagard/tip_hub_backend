# Django packages
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Third party apps
from ckeditor.fields import RichTextField
# Local apps
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('پست الکترونیکی'))
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('شماره تماس'))
    fullname = models.CharField(max_length=255, verbose_name=_('نام کامل'))
    bio = RichTextField(null=True, blank=True, verbose_name=_('درباره شما'))
    image = models.ImageField(upload_to='user/images/', null=True, blank=True,
                              verbose_name=_('عکس پروفایل'))
    age = models.IntegerField(default=1, verbose_name=_('سن'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    is_admin = models.BooleanField(default=False, verbose_name=_('مدیر سایت'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'fullname']

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربرها')

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
