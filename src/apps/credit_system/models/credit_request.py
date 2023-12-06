from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'CreditRequest',
)


class CreditRequest(models.Model):
    account_id = models.ForeignKey('account_system.Account', on_delete=models.CASCADE, related_name='accounts')
    amount = models.DecimalField(_('Amount of $'), decimal_places=2, max_digits=10)
    period = models.IntegerField(_('Amount of years'), validators=[MaxValueValidator(50)])
    request_timestamp = models.DateTimeField(_('Application date'), auto_now=True)
    approved = models.BooleanField(_('Approved'), blank=True)
    approved_timestamp = models.DateTimeField(_('The date of issuing approval of the application'), null=True,
                                              blank=True)
    manager_id = models.ForeignKey('account_system.User', on_delete=models.CASCADE, related_name='creditRequests')
    closed_timestamp = models.DateTimeField(_('The date of issuing approval of the application'), null=True,
                                              blank=True)

    class Meta:
        app_label = 'credit_system'
        verbose_name = _('CreditRequest')
        verbose_name_plural = _('CreditRequests')