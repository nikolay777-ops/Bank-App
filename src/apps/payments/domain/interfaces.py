import abc
from payments.domain.entities import PaymentTransactionEntity
from payments.models import PaymentTransaction


class IPaymentsProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_payment_transaction(
            self,
            entity: PaymentTransactionEntity
    ) -> PaymentTransaction | None:
        pass


class IPaymentDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_payment_transaction_by_pk(
            self,
            payment_transaction_pk: int
    ) -> PaymentTransactionEntity:
        pass
