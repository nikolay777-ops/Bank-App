from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'InvestmentStrategy',
)


class InvestmentStrategy(models.Model):
    investment_portfolio = models.OneToOneField('InvestmentPortfolio', on_delete=models.CASCADE)
    subscribe_commission = models.FloatField()
    revenue_commission = models.FloatField()

    class Meta:
        app_label = 'stocks'
        verbose_name = _('Investment Strategy')
        verbose_name_plural = _('Investment Strategies')
