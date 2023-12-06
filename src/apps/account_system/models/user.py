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
    qr_code = models.ImageField(upload_to='qrcode/', null=True, blank=True)
    otp_code = EncryptedCharField(_('OTP code'), max_length=100, null=True, blank=True)
    otp_code_updated_at = models.DateTimeField(_('Date and time of otp code update'), auto_now=True)
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='users')
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='users')

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'account_system'
        verbose_name = _('User')
        verbose_name_plural = _('Users')