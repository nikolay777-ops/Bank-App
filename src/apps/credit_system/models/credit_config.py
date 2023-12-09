from django.db import models

__all__ = (
    'CreditConfiguration'
)


class CreditConfiguration(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    currency = models.ForeignKey('account_system.Currency', on_delete=models.SET_NULL, null=True, related_name='+')
    name = models.CharField()

