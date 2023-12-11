from decimal import Decimal
from django.test import TestCase

import constants
from currency_rates.infrastructure.services.currency_account_processor import CurrencyAccountProcessor
from currency_rates.models import Currency
from currency_rates.models.currency_account import CurrencyAccount
from currency_rates.domain.entities import CurrencyAccountEntity
from currency_rates.infrastructure.daos.currency_account_dao import CurrencyAccountDAO
from user.models import User


class TestCurrencyAccountProcessor(TestCase):
    def setUp(self):
        self.processor = CurrencyAccountProcessor()
        self.currency = Currency.objects.create(name=constants.currency.CURRENCY_CODE_USD)
        self.user = User.objects.create(name='Nicko', phone_number='+375111111111', password='Kk12345678')
        self.currency_account = CurrencyAccount.objects.create(
            currency=self.currency,
            user=self.user,
            balance=1000,
        )
        self.entity = CurrencyAccountEntity(
            currency_pk=self.currency_account.currency.pk,
            user_pk=self.currency_account.user.pk,
            balance=self.currency_account.balance
        )

    def test_update_currency_account(self):
        new_balance = Decimal('1000.00')
        self.entity.balance = new_balance
        self.processor.update_currency_account(self.entity)
        currency_account = CurrencyAccount.objects.get(pk=self.currency_account.pk)
        assert currency_account.balance == new_balance
