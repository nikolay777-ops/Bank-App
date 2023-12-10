from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'CreditPayment',
)


class CreditPayment(models.Model):
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, related_name='credit_payment_credit', null=True)
    amount = models.DecimalField(_('The amount for payment'), decimal_places=2, max_digits=10)
    payment_timestamp = models.DateTimeField(_('Payment date'), auto_now_add=True)

    class Meta:
        app_label = 'credit_system'
        verbose_name = _('CreditPayment')
        verbose_name_plural = _('CreditPayments')