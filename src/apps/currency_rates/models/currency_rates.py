from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'CurrencyRate',
)


class CurrencyRate(models.Model):
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    rate = models.FloatField()
    date_of_use = models.DateTimeField()

    def __str__(self):
        return f'{self.currency.name}:{self.rate}{self.date_of_use}'

    class Meta:
        app_label = 'currency_rates'
        verbose_name = _('Currency rate')
        verbose_name_plural = _('Currency rates')
