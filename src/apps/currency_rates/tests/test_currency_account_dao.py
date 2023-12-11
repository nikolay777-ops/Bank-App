from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

import constants
from currency_rates.models import Currency
from currency_rates.models.currency_account import CurrencyAccount
from currency_rates.domain.entities import CurrencyAccountEntity
from currency_rates.infrastructure.daos.currency_account_dao import CurrencyAccountDAO
from user.models import User


class TestCurrencyAccountDAO(TestCase):
    def setUp(self):
        self.dao = CurrencyAccountDAO()
        self.currency = Currency.objects.create(name=constants.currency.CURRENCY_CODE_USD)
        self.user = User.objects.create(name='Nicko', phone_number='+375111111111', password='Kk12345678')
        self.currency_account = CurrencyAccount.objects.create(
            currency=self.currency,
            user=self.user,
            balance=1000,
        )

    def test_orm_to_entity(self):
        entity = self.dao._orm_to_entity(self.currency_account)
        assert isinstance(entity, CurrencyAccountEntity)
        assert entity.currency_pk == self.currency_account.currency.pk
        assert entity.user_pk == self.currency_account.user.pk
        assert entity.balance == self.currency_account.balance

    def test_fetch_all_by_user_pk(self):
        entities = self.dao.fetch_all_by_user_pk(self.currency_account.user.pk)
        assert isinstance(entities, list)
        assert all(isinstance(entity, CurrencyAccountEntity) for entity in entities)

    def test_fetch_by_user_pk_currency_pk(self):
        entity = self.dao.fetch_by_user_pk_currency_pk(self.currency_account.user.pk, self.currency_account.currency.pk)
        assert isinstance(entity, CurrencyAccountEntity)
        assert entity.currency_pk == self.currency_account.currency.pk
        assert entity.user_pk == self.currency_account.user.pk
        assert entity.balance == self.currency_account.balance

    def test_fetch_all_by_user_pk_no_accounts(self):
        user_pk = 999
        entities = self.dao.fetch_all_by_user_pk(user_pk)
        assert isinstance(entities, list)
        assert len(entities) == 0
