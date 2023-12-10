from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Account',
)


class Account(models.Model):
    amount = models.DecimalField(_('Amount of money'), decimal_places=2, max_digits=10)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='account_owner', null=True)

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        app_label = 'account_system'
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        unique_together = ('owner', 'currency')
