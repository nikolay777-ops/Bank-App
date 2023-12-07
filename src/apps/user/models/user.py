from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from django.utils.translation import gettext_lazy as _

__all__ = (
    'User',
)


class User(AbstractBaseUser):
    name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=13)
    qr_code = models.ImageField(upload_to='qrcode/', blank=True, null=True)
    otp_code = EncryptedCharField(_('OTP code'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(_('Date and time of creation'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date and time of update'), auto_now=True)
    otp_code_updated_at = models.DateTimeField(_('Date and time of otp code update'), auto_now=True)

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
