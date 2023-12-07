from payments.domain.entities import PaymentTransactionEntity
from payments.domain.interfaces import IPaymentDAO
from payments.models import PaymentTransaction


class PaymentDAO(IPaymentDAO):
    def _orm_to_entity(
            self,
            orm_object: PaymentTransaction
    ) -> PaymentTransactionEntity:
        entity = PaymentTransactionEntity(
            payment_pk=orm_object.payment.pk,
            sender_pk=orm_object.sender.pk,
            count=orm_object.count
        )

        return entity

    def fetch_payment_transaction_by_pk(
            self,
            payment_transaction_pk: int
    ) -> PaymentTransactionEntity:
        obj = PaymentTransaction.objects.filter(pk=payment_transaction_pk)

        if obj:
            obj = self._orm_to_entity(orm_object=obj)

            return obj

        return None
