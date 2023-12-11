from dataclasses import dataclass
from decimal import Decimal

@dataclass
class AccountEntity:
    currency_pk: int
    owner_pk: int
    amount: Decimal