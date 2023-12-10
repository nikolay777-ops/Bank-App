from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from django.utils.translation import gettext_lazy as _

__all__ = (
    'User',
)

from account_system.manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=13, unique=True)
    secret_code = EncryptedCharField(_('secret code'), max_length=100, null=True, blank=True)
    secret_code_updated_at = models.DateTimeField(_('Date and time of secret code update'), auto_now=True)
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='users', default=1, null=True)

    USERNAME_FIELD = 'phone_number'
    objects = MyUserManager()

    @property
    def is_staff(self):
        return True

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'account_system'
        verbose_name = _('User')
        verbose_name_plural = _('Users')