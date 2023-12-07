from dataclasses import dataclass


@dataclass
class PaymentTransactionEntity:
    payment_pk: int
    sender_pk: int
    count: float
