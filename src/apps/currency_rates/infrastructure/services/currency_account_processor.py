from abc import ABC

from django.core.exceptions import ObjectDoesNotExist

from currency_rates.domain.entities import CurrencyAccountEntity
from currency_rates.domain.interfaces import ICurrencyAccountProcessor
from currency_rates.models.currency_account import CurrencyAccount


class CurrencyAccountProcessor(ICurrencyAccountProcessor, ABC):
    def update_currency_account(self, entity: CurrencyAccountEntity):
        try:
            obj = CurrencyAccount.objects.get(
                currency_id=entity.currency_pk,
                user_id=entity.user_pk,
            )

            obj.balance = entity.balance
            obj.save()
        except ObjectDoesNotExist:
            print(f"The object with pk={entity.currency_pk} does not exist")
