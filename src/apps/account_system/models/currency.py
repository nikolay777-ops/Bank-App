from django.db import models

import constants.currency
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Currency',
)


class Currency(models.Model):
    name = models.CharField(primary_key=True, choices=constants.currency.ALL_CURRENCY_CODES_CHOICES)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        app_label = 'account_system'
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
