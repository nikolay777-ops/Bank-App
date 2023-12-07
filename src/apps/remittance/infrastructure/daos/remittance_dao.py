from django.core.exceptions import ObjectDoesNotExist

from remittance.domain.entities import RemittanceEntity
from remittance.domain.interfaces import IRemittanceDAO
from remittance.models.remittance import Remittance


class RemittanceDAO(IRemittanceDAO):
    def _orm_to_entity(self, orm_object: Remittance) -> RemittanceEntity:
        entity = RemittanceEntity(
            pk=orm_object.pk,
            currency_pk=orm_object.currency.pk,
            sender_pk=orm_object.sender.pk,
            receiver_pk=orm_object.receiver.pk,
            count=orm_object.count,
        )

        return entity

    def fetch_remittance_by_pk(self, remittance_pk: int) -> RemittanceEntity:
        try:
            obj = Remittance.objects.get(pk=remittance_pk)
            if not obj.accepted:
                entity = self._orm_to_entity(orm_object=obj)

                return entity

            return None
        except ObjectDoesNotExist:
            print(f'Required remittance {remittance_pk} does not exist')