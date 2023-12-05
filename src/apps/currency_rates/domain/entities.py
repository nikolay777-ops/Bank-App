import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CurrencyRateEntity:
    currency: str
    rate: Decimal
    date_of_use: datetime.datetime
