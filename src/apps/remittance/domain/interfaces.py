import abc
from remittance.domain.entities import RemittanceEntity


class IRemittanceProcessor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_remittance(self, entity: RemittanceEntity):
        pass

    @abc.abstractmethod
    def accept_remittance(self, remittance_pk: int):
        pass

    @abc.abstractmethod
    def update_remittance(self, entity: RemittanceEntity, success: bool):
        pass


class IRemittanceDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_remittance_by_pk(self, remittance_pk: int) -> RemittanceEntity:
        pass
