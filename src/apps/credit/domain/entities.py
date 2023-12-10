from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreditPaymentEntity:
    credit_pk: int
    amount: Decimal
    interest_rate: Decimal
    term_month: int
    monthly_payment: Decimal
    currency: str
    available_cash: Decimal

