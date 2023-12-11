import abc
from transaction_system.domain.entities import TransactionEntity


class ITransactionProcessor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_transaction(self, entity: TransactionEntity):
        pass

    @abc.abstractmethod
    def accept_transaction(self, transaction_pk: int):
        pass

    @abc.abstractmethod
    def update_transaction(self, entity: TransactionEntity, success: bool):
        pass


class ITransactionDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_transaction_by_pk(self, transaction_pk: int) -> TransactionEntity:
        pass