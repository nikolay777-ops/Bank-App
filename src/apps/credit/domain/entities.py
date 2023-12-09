from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreditPayEntity:
    pk: int
    amount: Decimal
    interest_rate: Decimal
    term_month: int
    currency: str
    available_cash: Decimal
