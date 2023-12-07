from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.translation import gettext_lazy as _


__all__ = (
    'StockTransaction',
)


class StockTransaction(models.Model):
    buy = models.BooleanField(default=True)
    inv_portfolio = models.ForeignKey(
        'InvestmentPortfolio',
        on_delete=models.SET_NULL,
        related_name='transaction_inv_port',
        null=True,
    )
    stock_price = models.OneToOneField('StockPrices', on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        app_label = 'stocks'
        verbose_name = _('Stock transaction')
        verbose_name_plural = _('Stock transactions')

