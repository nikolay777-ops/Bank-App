from django.core.exceptions import ObjectDoesNotExist

from account_system.domain.entities import AccountEntity
from account_system.domain.interfaces import IAccountDAO
from account_system.models import Account


class AccountDAO(IAccountDAO):

    def _orm_to_entity(
            self,
            orm_obj: Account
    ) -> AccountEntity:
        entity = AccountEntity(
            currency_pk=orm_obj.currency.pk,
            owner_pk=orm_obj.owner.pk,
            amount=orm_obj.amount
        )

        return entity

    def fetch_all_by_owner_pk(
            self,
            owner_pk: int
    ) -> list[AccountEntity]:
        account_obj_list = Account.objects.filter(owner_id=owner_pk)

        account_entity_list = [
            self._orm_to_entity(orm_obj=obj)
            for obj in account_obj_list
        ]

        return account_entity_list

    def fetch_by_owner_pk_currency_pk(
            self,
            owner_pk: int,
            currency_pk: str
    ) -> AccountEntity:
        try:
            obj = Account.objects.get(owner_id=owner_pk, currency_id=currency_pk)
            entity = self._orm_to_entity(orm_obj=obj)
            return entity
        except ObjectDoesNotExist:
            print(f'Requested owner: {owner_pk} does not have an account with currency: {currency_pk}')
            return None
