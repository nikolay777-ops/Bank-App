from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'GeneralConfig',
)


class GeneralConfig(models.Model):
    credit_interest = models.DecimalField(_('The interest rate of the credit'), decimal_places=2, max_digits=3,
                                          validators=[MinValueValidator(0.00), MaxValueValidator(1.00)])

    class Meta:
        app_label = 'credit_system'
        verbose_name = _('GeneralConfig')
        verbose_name_plural = _('GeneralConfigs')