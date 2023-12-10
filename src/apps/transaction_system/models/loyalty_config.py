from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'LoyaltyConfig',
)


class LoyaltyConfig(models.Model):
    min = models.DecimalField(_('min amount of money'), decimal_places=2, max_digits=10)
    percent = models.DecimalField(_('%'), decimal_places=2, max_digits=3, default=0)


    def __str__(self):
        return f'{self.pk}{self.min}'
    class Meta:
        app_label = 'transaction_system'
        verbose_name = _('LoyaltyConfig')
        verbose_name_plural = _('LoyaltyConfigs')



