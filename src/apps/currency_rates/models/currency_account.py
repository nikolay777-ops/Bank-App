from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'CurrencyAccount',
)

import constants.currency


class CurrencyAccount(models.Model):
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.SET_DEFAULT,
        default=constants.currency.CURRENCY_CODE_USDT
    )
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='+')
    balance = models.FloatField()

    def __str__(self):
        return f'{self.user} {self.currency} {self.balance}'

    class Meta:
        app_label = 'currency_rates'
        verbose_name = _('Currency Account')
        verbose_name_plural = _('Currency Accounts')
        unique_together = ('currency', 'user')
