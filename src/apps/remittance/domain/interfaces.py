import abc

from remittance.domain.entities import RemittanceEntity


class IRemittanceProcessing(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_remittance(self, entity: RemittanceEntity):
        pass

    @abc.abstractmethod
    def accept_remittance(self, remittance_pk: int):
        pass

    @abc.abstractmethod
    def decline_remittance(self, remittance_pk: int):
        pass
