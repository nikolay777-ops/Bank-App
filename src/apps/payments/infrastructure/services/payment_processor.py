from payments.domain.entities import PaymentTransactionEntity
from payments.domain.interfaces import IPaymentsProcessor
from payments.models import PaymentTransaction


class PaymentProcessor(IPaymentsProcessor):
    def create_payment_transaction(self, entity: PaymentTransactionEntity) -> PaymentTransaction | None:
        obj = PaymentTransaction.objects.create(
            payment_id=entity.payment_pk,
            sender_id=entity.sender_pk,
            count=entity.count
        )

        return obj
