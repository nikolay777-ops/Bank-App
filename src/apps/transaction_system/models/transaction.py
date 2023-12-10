from django.db import models
from django.utils.translation import gettext_lazy as _
from account_system.models.currency import Currency

__all__ = (
    'Transaction',
)


class Transaction(models.Model):
    currency = models.ForeignKey('account_system.Currency', on_delete=models.CASCADE, null=True, related_name='transactions_currency')
    corespondent_id = models.ForeignKey('account_system.User', on_delete=models.CASCADE, related_name='transactions_corespondents')
    recipient_id = models.ForeignKey('account_system.User', on_delete=models.CASCADE, related_name='transactions_recipients')
    amount = models.DecimalField(_('Amount of money'), decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(_('The date of the transaction'))
    commission = models.DecimalField(_('Commission'), decimal_places=2, max_digits=10, null=True)
    success = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}{self.currency}'
    class Meta:
        app_label = 'transaction_system'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')



