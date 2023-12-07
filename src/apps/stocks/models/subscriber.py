from django.db import models

__all__ = (
    'Subscriber',
)


class Subscriber(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='subscriber_user')
    strategy = models.ForeignKey('InvestmentStrategy', on_delete=models.CASCADE)
