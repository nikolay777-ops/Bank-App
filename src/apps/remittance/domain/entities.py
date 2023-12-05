import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RemittanceEntity:
    sender_pk: int
    reciever_pk: int
    count: Decimal
    dt: datetime.datetime

