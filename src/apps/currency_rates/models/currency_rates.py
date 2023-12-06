from django.db import models
from django.utils.translation import gettext_lazy as _
from currency_rates.models.currency import Currency

class CurrencyRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=8, decimal_places=5)
    date_of_use = models.DateTimeField()

    def __str__(self):
        return f'{self.currency.name}:{self.rate}{self.date_of_use}'

    class Meta:
        app_label = 'currency_rates'
        verbose_name = _('Currency rate')
        verbose_name_plural = _('Currency rates')
        