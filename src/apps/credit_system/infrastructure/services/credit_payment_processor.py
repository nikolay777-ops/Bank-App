from decimal import Decimal

from credit_system.domain.entities import CreditPaymentEntity
from credit_system.models import Credit, CreditPayment


class CreditPaymentProcessor:
    def count_montly_payment(
            self,
            payment_entity: CreditPaymentEntity,
            amount: Decimal
    ) -> Decimal:
        monthly_payment = Decimal(
            (payment_entity.amount - amount) / payment_entity.term_month
        )

        return monthly_payment

    def create_credit_payment(
            self,
            payment_entity: CreditPaymentEntity,
            amount: Decimal
    ):
        credit = Credit.objects.get(pk=payment_entity.credit_pk)
        if amount >= credit.remaining_amount:
            credit.currency_account.amount -= credit.remaining_amount
            credit.remaining_amount = 0

        else:
            credit.remaining_amount -= amount
            credit.currency_account.amount -= amount
            monthly_payment = self.count_montly_payment(payment_entity, amount)
            credit.monthly_payment = monthly_payment

        if credit.remaining_amount == 0:
            credit.closed = True

        credit.save()
        credit.currency_account.save()

        CreditPayment.objects.create(
            credit=credit,
            amount=amount
        )