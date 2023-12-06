from django.db import models
from django.utils.translation import gettext_lazy as _
from .role import Role
from .permission import Permission
__all__ = (
    'RolesPermissions',
)


class RolesPermissions(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        app_label = 'account_system'
        verbose_name = _('RolesPermissions')
        verbose_name_plural = _('RolesPermissions')