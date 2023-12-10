from decimal import Decimal

from credit_system.domain.entities import CreditPaymentEntity
from credit_system.models import Credit
from account_system.models import Account


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
        credits = Credit.objects.filter(currency_account__owner__phone_number=phone_num, closed=False)
        account_cash_amounts = Account.objects.filter(
            owner__phone_number=phone_num,
            currency__name__in=credits.values_list('configuration__currency__name', flat=True)
        ).values_list('amount', flat=True)

        credit_pay_entity_list = [
            self._orm_to_entity(credit, amount)
            for credit, amount in zip(credits, account_cash_amounts)
        ]

        return credit_pay_entity_list

    def fetch_by_credit_pk(self, credit_pk: int) -> CreditPaymentEntity:
        credit = Credit.objects.get(pk=credit_pk, closed=False)
        currency_account = Account.objects.get(
            owner=credit.currency_account.owner,
            currency__name=credit.configuration.currency.name
        )

        entity = self._orm_to_entity(credit, amount=currency_account.amount)

        return entity