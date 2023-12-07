from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BalanceEntity:
    user_pk: int
    currency: str
    count: Decimal


@dataclass
class ContactEntity:
    from_user_pk: int
    to_user_pk: int
    is_close: bool


@dataclass
class UserEntity:
    pk: int
    name: str
    bank_accounts: list[BalanceEntity]
