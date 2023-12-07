from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Transaction',
)


class Transaction(models.Model):
    corespondent_id = models.ForeignKey('account_system.User', on_delete=models.CASCADE, related_name='transactions_corespondents')
    recipient_id = models.ForeignKey('account_system.User', on_delete=models.CASCADE, related_name='transactions_recipients')
    amount = models.DecimalField(_('Amount of $'), decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(_('The date of the transaction'))

    class Meta:
        app_label = 'transaction_system'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')