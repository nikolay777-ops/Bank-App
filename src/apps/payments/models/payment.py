from django.db import models
from django.utils.translation import gettext_lazy as _

from constants.payments import ALL_PAYMENT_CODES_CHOICES

__all__ = (
    'Payment'
)


class Payment(models.Model):
    name = models.CharField(
        primary_key=True,
        choices=ALL_PAYMENT_CODES_CHOICES
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'payments'
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
