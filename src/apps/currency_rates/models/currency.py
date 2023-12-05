from django.db import models
from django.utils.translation import gettext_lazy as _
from constants.currency import ALL_CURRENCY_CODES_CHOICES

__all__ = (
    'Currency'
)


class Currency(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=4,
        choices=ALL_CURRENCY_CODES_CHOICES,
        primary_key=True,
        help_text=_('Currency name from ALL_CURRENCIES list')
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'currency_rates'
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
