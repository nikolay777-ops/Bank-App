from decimal import Decimal

from credit.domain.entities import CreditPayEntity
from credit.models import Credit
from currency_rates.models import CurrencyAccount


class CreditPayDAO:
    def _orm_to_entity(self, orm_obj: Credit, amount: Decimal):
        entity = CreditPayEntity(
            pk=orm_obj.pk,
            amount=orm_obj.remaining_amount,
            interest_rate=100 * orm_obj.configuration.interest_rate,
            term_month=orm_obj.configuration.term_months,
            currency=orm_obj.configuration.currency.name,
            available_cash=amount
        )

        return entity

    def fetch_by_phone_number(self, phone_num: str) -> list[CreditPayEntity]:
        credits = Credit.objects.filter(user__phone_number=phone_num)
        account_cash_amounts = CurrencyAccount.objects.filter(
            user__phone_number=phone_num,
            currency__name__in=credits.values_list('configuration__currency__name', flat=True)
        ).values_list('balance', flat=True)

        credit_pay_entity_list = [
            self._orm_to_entity(credit, amount)
            for credit, amount in zip(credits, account_cash_amounts)
        ]

        return credit_pay_entity_list


