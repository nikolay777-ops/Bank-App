from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TransactionEntity:
    pk: int
    currency_pk: str
    recipient_pk: int
    corespondent_pk: int
    amount: Decimal