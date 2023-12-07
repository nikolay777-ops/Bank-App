from django.core.exceptions import ObjectDoesNotExist

from currency_rates.domain.entities import CurrencyAccountEntity
from currency_rates.domain.interfaces import ICurrencyAccountDAO
from currency_rates.models.currency_account import CurrencyAccount


class CurrencyAccountDAO(ICurrencyAccountDAO):

    def _orm_to_entity(
            self,
            orm_obj: CurrencyAccount
    ) -> CurrencyAccountEntity:
        entity = CurrencyAccountEntity(
            currency_pk=orm_obj.currency.pk,
            user_pk=orm_obj.user.pk,
            balance=orm_obj.balance
        )

        return entity

    def fetch_all_by_user_pk(
            self,
            user_pk: int
    ) -> list[CurrencyAccountEntity]:
        currency_account_obj_list = CurrencyAccount.objects.filter(user_id=user_pk)

        currency_account_entity_list = [
            self._orm_to_entity(orm_obj=obj)
            for obj in currency_account_obj_list
        ]

        return currency_account_entity_list

    def fetch_by_user_pk_currency_pk(
            self,
            user_pk: int,
            currency_pk: str
    ) -> CurrencyAccountEntity:

        try:
            obj = CurrencyAccount.objects.get(user_id=user_pk, currency_id=currency_pk)
            entity = self._orm_to_entity(orm_obj=obj)

            return entity

        except ObjectDoesNotExist:
            print(f'Requested user: {user_pk} has not {currency_pk} account')
