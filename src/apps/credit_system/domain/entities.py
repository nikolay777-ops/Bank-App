from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreditViewEntity:
    name: str
    amount: Decimal
    interest_rate: Decimal
    term_month: int
