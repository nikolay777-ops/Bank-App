import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class StockEntity:
    name: str
    rate: Decimal
    data_of_use: datetime.datetime
    count: int
    profit: Decimal


@dataclass
class InvestmentPortfolioEntity:
    owner_pk: int
    name: str
    stocks: list[StockEntity]


@dataclass
class InvestmentStrategyEntity:
    inv_port_pk: int
    subscribe_commission: float
    revenue_commission: float
