from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from account_system.infrastructure.daos.account_dao import AccountDAO
from account_system.infrastructure.services.account_processor import AccountProcessor
from transaction_system.domain.entities import TransactionEntity
from transaction_system.domain.interfaces import ITransactionProcessor
from transaction_system.infrastructure.daos.transaction_dao import TransactionDAO
from transaction_system.models import Transaction


class TransactionProcessor(ITransactionProcessor):
    def __init__(self):
        self.account_dao = AccountDAO()
        self.account_processor = AccountProcessor()
        self.transaction_dao = TransactionDAO()

    def create_transaction(self, entity: TransactionEntity) -> Transaction:
        obj = Transaction.objects.create(
            currency_id=entity.currency_pk,
            corespondent_id=entity.corespondent_pk,
            recipient_id=entity.recipient_pk,
            amount=entity.amount,
            commission=Decimal(entity.amount * 0.015)
        )

        return obj if obj else None

    def update_transaction(self, entity: TransactionEntity, success: bool):
        try:
            obj = Transaction.objects.get(id=entity.pk)
            obj.success = success
            obj.accepted = success
            obj.save()

        except ObjectDoesNotExist:
            print(f"Transaction object {entity.pk} does not exist")

    def accept_transaction(self, transaction_pk: int):
        transaction_entity = self.transaction_dao.fetch_transaction_by_pk(
            transaction_pk=transaction_pk
        )

        if transaction_entity:
            corespondent_account_entity = self.account_dao.fetch_by_owner_pk_currency_pk(
                owner_pk=transaction_entity.corespondent_pk, currency_pk=transaction_entity.currency_pk)

            recipient_account_entity = self.account_dao.fetch_by_owner_pk_currency_pk(
                owner_pk=transaction_entity.recipient_pk, currency_pk=transaction_entity.currency_pk)

            corespondent_account_entity.amount -= transaction_entity.amount

            if corespondent_account_entity.amount >= 0 and recipient_account_entity:
                recipient_account_entity.amount += transaction_entity.amount

                self.account_processor.update_account(
                    entity=corespondent_account_entity
                )
                self.account_processor.update_account(
                    entity=recipient_account_entity
                )
                self.update_transaction(entity=transaction_entity, success=True)

            else:
                self.update_transaction(entity=transaction_entity, success=False)