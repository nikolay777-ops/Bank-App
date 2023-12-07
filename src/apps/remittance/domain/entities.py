import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RemittanceEntity:
    pk: int
    currency_pk: str
    sender_pk: int
    receiver_pk: int
    count: Decimal
