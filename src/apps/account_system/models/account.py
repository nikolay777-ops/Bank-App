from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Account',
)


class Account(models.Model):
    amount = models.DecimalField(_('Amount of $'), decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        app_label = 'account_system'
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')