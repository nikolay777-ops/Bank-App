import abc
from account_system.domain.entities import AccountEntity


class IAccountProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update_account(self, entity: AccountEntity):
        pass


class IAccountDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_all_by_owner_pk(
            self,
            owner_pk: int
    ) -> list[AccountEntity]:
        pass

    @abc.abstractmethod
    def fetch_by_owner_pk_currency_pk(
            self,
            owner_pk: int,
            currency_pk: str
    ) -> AccountEntity:
        pass