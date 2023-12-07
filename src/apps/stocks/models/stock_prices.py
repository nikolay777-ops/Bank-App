from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'StockPrices',
)


class StockPrices(models.Model):
    stock = models.OneToOneField('Stock', on_delete=models.CASCADE)
    rate = models.FloatField()
    date_of_use = models.DateTimeField()

    class Meta:
        app_label = 'stocks'
        verbose_name = _('Stock price')
        verbose_name_plural = _('Stock prices')
