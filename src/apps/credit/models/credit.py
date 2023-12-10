from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Credit',
)


class Credit(models.Model):
    currency_account = models.ForeignKey(
        'currency_rates.CurrencyAccount',
        related_name='credit_currency_account',
        on_delete=models.SET_NULL,
        null=True
    )
    configuration = models.ForeignKey(
        'CreditConfiguration',
        on_delete=models.CASCADE,
        related_name='credit_configuration'
    )
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'credit'
        verbose_name = _('Credit')
        verbose_name_plural = _('Credits')