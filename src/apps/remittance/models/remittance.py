from django.db import models
from django.utils.translation import gettext_lazy as _
from currency_rates.models.currency import Currency
from user.models import User


class Remittance(models.Model):
    currency = models.OneToOneField(Currency, on_delete=models.SET_NULL)
    sender = models.OneToOneField(User, on_delete=models.SET_NULL)
    reciever = models.OneToOneField(User, on_delete=models.SET_NULL)
    count = models.DecimalField(max_digits=6, decimal_places=2)
    comission = models.DecimalField(max_digits=5, decimal_places=2)
    success = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}{self.currency}'

    class Meta:
        app_label = 'remittance'
        verbose_name = _('Remittance')
        verbose_name_plural = _('Remittances')

