from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Role',
)


class Role(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(_('Description of role'), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'account_system'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')