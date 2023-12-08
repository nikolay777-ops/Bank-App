from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'InvestmentPortfolio',
)


class InvestmentPortfolio(models.Model):
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='portfolio_user')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.owner.name}: {self.name}'

    class Meta:
        app_label = 'stocks'
        verbose_name = _('Investment portfolio')
        verbose_name_plural = _('Investment portfolios')
