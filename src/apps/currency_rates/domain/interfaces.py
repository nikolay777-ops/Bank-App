import abc
from currency_rates.domain.entities import CurrencyTransactionEntity, CurrencyRateEntity, CurrencyAccountEntity
from currency_rates.models.currency_rates import CurrencyRate
from currency_rates.models.currency_transaction import CurrencyTransaction


class ICurrencyRateDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_latest_all(self) -> list[CurrencyRateEntity]:
        pass

    @abc.abstractmethod
    def fetch_latest_by_currency_pk(
            self,
            currency_pk: str
    ) -> CurrencyRateEntity:
        pass


class ICurrencyRateProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_currency_rate(self, entity: CurrencyRateEntity) -> CurrencyRate | None:
        pass


class ICurrencyTransactionProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_transaction(self, entity: CurrencyTransactionEntity) -> CurrencyTransaction | None:
        pass


class ICurrencyAccountProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update_currency_account(self, entity: CurrencyAccountEntity):
        pass


class ICurrencyAccountDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_all_by_user_pk(
            self,
            user_pk: int
    ) -> list[CurrencyAccountEntity]:
        pass

    @abc.abstractmethod
    def fetch_by_user_pk_currency_pk(
            self,
            user_pk: int,
            currency_pk: str
    ) -> CurrencyAccountEntity:
        pass
