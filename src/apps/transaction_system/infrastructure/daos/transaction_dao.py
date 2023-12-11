from django.core.exceptions import ObjectDoesNotExist

from transaction_system.domain.entities import TransactionEntity
from transaction_system.domain.interfaces import ITransactionDAO
from transaction_system.domain.interfaces import ITransactionDAO
from transaction_system.models import Transaction


class TransactionDAO(ITransactionDAO):
    def _orm_to_entity(self, orm_object: Transaction) -> TransactionEntity:
        entity = TransactionEntity(
            pk=orm_object.pk,
            currency_pk=orm_object.currency.pk,
            corespondent_pk=orm_object.corespondent_id.pk,
            recipient_pk=orm_object.recipient_id.pk,
            amount=orm_object.amount,
        )

        return entity

    def fetch_transaction_by_pk(self, transaction_pk: int) -> TransactionEntity:
        try:
            obj = Transaction.objects.get(pk=transaction_pk)
            if not obj.accepted:
                entity = self._orm_to_entity(orm_object=obj)

                return entity

            return None
        except ObjectDoesNotExist:
            print(f'Required transaction {transaction_pk} does not exist')