from django.db import models
from django.utils.translation import gettext_lazy as _


__all__ = (
    'CreditConfiguration'
)


class CreditConfiguration(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    currency = models.ForeignKey('currency_rates.Currency', on_delete=models.SET_NULL, null=True, related_name='+')
    name = models.CharField()

    def __str__(self):
        return f'{self.currency} Amount:{self.amount} Rate:{self.interest_rate} Term month: {self.term_months}'

    class Meta:
        app_label = 'credit'
        verbose_name = _('Credit Configuration')
        verbose_name_plural = _('Credit Configurations')
