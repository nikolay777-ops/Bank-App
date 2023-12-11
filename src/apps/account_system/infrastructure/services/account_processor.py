from abc import ABC

from django.core.exceptions import ObjectDoesNotExist

from account_system.domain.entities import AccountEntity
from account_system.domain.interfaces import IAccountProcessor
from account_system.models.account import Account


class AccountProcessor(IAccountProcessor, ABC):
    def update_account(self, entity: AccountEntity):
        try:
            obj = Account.objects.get(
                currency_id=entity.currency_pk,
                owner_id=entity.owner_pk,
            )

            obj.amount = entity.amount
            obj.save()
        except ObjectDoesNotExist:
            print(f"The object with pk={entity.currency_pk} does not exist")