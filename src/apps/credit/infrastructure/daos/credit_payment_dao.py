from decimal import Decimal

from credit.domain.entities import CreditPaymentEntity
from credit.models import Credit
from currency_rates.models import CurrencyAccount


class CreditPaymentDAO:
    def _orm_to_entity(self, orm_obj: Credit, amount: Decimal):
        entity = CreditPaymentEntity(
            credit_pk=orm_obj.pk,
            amount=orm_obj.remaining_amount,
            interest_rate=100 * orm_obj.configuration.interest_rate,
            term_month=orm_obj.configuration.term_months,
            currency=orm_obj.configuration.currency.name,
            available_cash=amount,
            monthly_payment=orm_obj.monthly_payment
        )

        return entity

    def fetch_by_phone_number(self, phone_num: str) -> list[CreditPaymentEntity]:
        credits = Credit.objects.filter(currency_account__user__phone_number=phone_num, closed=False)
        account_cash_amounts = CurrencyAccount.objects.filter(
            user__phone_number=phone_num,
            currency__name__in=credits.values_list('configuration__currency__name', flat=True)
        ).values_list('balance', flat=True)

        credit_pay_entity_list = [
            self._orm_to_entity(credit, amount)
            for credit, amount in zip(credits, account_cash_amounts)
        ]

        return credit_pay_entity_list

    def fetch_by_credit_pk(self, credit_pk: int) -> CreditPaymentEntity:
        credit = Credit.objects.get(pk=credit_pk, closed=False)
        currency_account = CurrencyAccount.objects.get(
            user=credit.currency_account.user,
            currency__name=credit.configuration.currency.name
        )

        entity = self._orm_to_entity(credit, amount=currency_account.balance)

        return entity
