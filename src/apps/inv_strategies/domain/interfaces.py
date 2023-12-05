import abc
from decimal import Decimal


class IInvestmentStrategyProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_investment_strategy(
            self,
            investment_port_pk: int,
            subscribe_commission: Decimal,
            revenue_commission: Decimal
    ):
        pass

    @abc.abstractmethod
    def delete_investment_strategy(
            self,
            pk: int
    ):
        pass

    @abc.abstractmethod
    def fetch_all_investment_strategies(
            self,
            user_pk: int
    ) -> list[InvestmentStrategyEntity]:
        pass
