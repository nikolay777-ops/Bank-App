import abc
from decimal import Decimal

from stocks.domain.entities import InvestmentStrategyEntity, InvestmentPortfolioEntity


class IInvestmentStrategyProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_investment_strategy(
            self,
            entity: InvestmentStrategyEntity
    ) -> InvestmentStrategyEntity | None:
        pass

    @abc.abstractmethod
    def delete_investment_strategy(
            self,
            obj_pk: int
    ):
        pass


class IInvestmentStrategySubscriberProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_investment_strategy_subscriber(
            self,
            investment_strategy_pk: int,
            subscriber_pk: int
    ):
        pass

    @abc.abstractmethod
    def remove_investment_strategy_subscriber(
            self,
            investment_strategy_pk: int,
            subscriber_pk: int
    ):
        pass


class IInvestmentStrategyDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_all_by_user_pk(
            self,
            user_pk: int
    ) -> list[InvestmentStrategyEntity]:
        pass


class IInvestmentPortfolioDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_by_user_pk(self, pk: int) -> list[InvestmentPortfolioEntity]:
        pass

    @abc.abstractmethod
    def fetch_by_portfolio_pk(self, portfolio_pk: int) -> InvestmentPortfolioEntity:
        pass
