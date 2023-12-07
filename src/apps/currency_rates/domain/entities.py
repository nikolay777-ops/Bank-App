import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CurrencyRateEntity:
    pk: int
    currency: str
    rate: Decimal
    date_of_use: datetime.datetime


@dataclass
class CurrencyTransactionEntity:
    user_pk: int
    currency_rate: CurrencyRateEntity
    count: int


@dataclass
class CurrencyAccountEntity:
    currency_pk: int
    user_pk: int
    balance: Decimal
