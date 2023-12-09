from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Credit',
)

from account_system.models import User


class Credit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_credit',
        on_delete=models.CASCADE,
    )
    configuration = models.ForeignKey(
        'CreditConfiguration',
        on_delete=models.CASCADE,
        related_name='credit_configuration'
    )
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'credit_system'
        verbose_name = _('Credit')
        verbose_name_plural = _('Credits')
        unique_together = ('user', 'configuration')
