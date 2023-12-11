from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from currency_rates.infrastructure.daos.currency_account_dao import CurrencyAccountDAO
from currency_rates.infrastructure.services.currency_account_processor import CurrencyAccountProcessor
from remittance.domain.entities import RemittanceEntity
from remittance.domain.interfaces import IRemittanceProcessor
from remittance.infrastructure.daos.remittance_dao import RemittanceDAO
from remittance.models.remittance import Remittance


class RemittanceProcessor(IRemittanceProcessor):
    def __init__(self):
        self.currency_account_dao = CurrencyAccountDAO()
        self.currency_account_processor = CurrencyAccountProcessor()
        self.remittance_dao = RemittanceDAO()

    def create_remittance(self, entity: RemittanceEntity) -> Remittance:
        obj = Remittance.objects.create(
            currency_id=entity.currency_pk,
            sender_id=entity.sender_pk,
            receiver_id=entity.receiver_pk,
            count=entity.count,
            commission=Decimal(entity.count) * Decimal(0.015)
        )

        return obj if obj else None

    def update_remittance(self, entity: RemittanceEntity, success: bool):
        try:
            obj = Remittance.objects.get(id=entity.pk)
            obj.success = success
            obj.accepted = success
            obj.save()

        except ObjectDoesNotExist:
            print(f"Remittance object {entity.pk} does not exist")

    def accept_remittance(self, remittance_pk: int):
        remittance_entity = self.remittance_dao.fetch_remittance_by_pk(
            remittance_pk=remittance_pk
        )

        if remittance_entity:
            sender_currency_account_entity = self.currency_account_dao.fetch_by_user_pk_currency_pk(
                user_pk=remittance_entity.sender_pk,
                currency_pk=remittance_entity.currency_pk
            )

            receiver_currency_account_entity = self.currency_account_dao.fetch_by_user_pk_currency_pk(
                user_pk=remittance_entity.receiver_pk,
                currency_pk=remittance_entity.currency_pk
            )

            sender_currency_account_entity.balance -= Decimal(remittance_entity.count)

            if sender_currency_account_entity.balance >= 0 and receiver_currency_account_entity:
                receiver_currency_account_entity.balance += Decimal(remittance_entity.count)

                self.currency_account_processor.update_currency_account(
                    entity=sender_currency_account_entity
                )
                self.currency_account_processor.update_currency_account(
                    entity=receiver_currency_account_entity
                )
                self.update_remittance(entity=remittance_entity, success=True)

            else:
                self.update_remittance(entity=remittance_entity, success=False)
