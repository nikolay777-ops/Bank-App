from django.db import models
from django.utils.translation import gettext_lazy as _
from constants.stocks import ALL_STOCK_CHOICES

__all__ = (
    'Stock',
)


class Stock(models.Model):
    name = models.CharField(primary_key=True, choices=ALL_STOCK_CHOICES, max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'stocks'
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
