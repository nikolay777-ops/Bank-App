from django.db import models
from django.utils.translation import gettext_lazy as _
from currency_rates.models.currency import Currency
from user.models import User

__all__ = (
    'Remittance',
)


class Remittance(models.Model):
    currency = models.OneToOneField(Currency, on_delete=models.SET_NULL, null=True, related_name='+')
    sender = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='remittance_sender')
    receiver = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='remittance_receiver')
    count = models.FloatField()
    commission = models.FloatField()
    success = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}{self.currency}'

    class Meta:
        app_label = 'remittance'
        verbose_name = _('Remittance')
        verbose_name_plural = _('Remittances')
