from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'PaymentTransaction',
)


class PaymentTransaction(models.Model):
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, related_name='+', null=True)
    sender = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    count = models.FloatField()
    created_at = models.DateTimeField(
        _('Date and time of creation'),
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.payment.name}:{self.sender.id}:{self.count}'

    class Meta:
        app_label = 'payments'
        verbose_name = _('Payment Transaction')
        verbose_name_plural = _('Payment Transactions')
