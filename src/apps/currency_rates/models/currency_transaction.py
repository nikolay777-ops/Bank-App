from django.db import models
from django.utils.translation import gettext_lazy as _

from currency_rates.models.currency_rates import CurrencyRate
from user.models import User

__all__ = (
    'CurrencyTransaction',
)


class CurrencyTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True)
    currency_rate = models.OneToOneField(CurrencyRate, on_delete=models.SET_NULL, null=True)
    count = models.FloatField()

    def __str__(self):
        name = self.currency_rate.currency.name
        return f'{self.user.pk}:{name}:{self.currency_rate.rate} Count: {self.count}'

    class Meta:
        app_label = 'currency_rates'
        verbose_name = _('Currency Transaction')
        verbose_name_plural = _('Currency Transactions')
