from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Permission',
)


class Permission(models.Model):
    description = models.CharField(_('Description of permission'), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'account_system'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')