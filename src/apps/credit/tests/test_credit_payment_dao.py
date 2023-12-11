import pytest
from decimal import Decimal
from django.test import TestCase

import constants.currency
from credit.models import Credit, CreditConfiguration
from credit.domain.entities import CreditPaymentEntity
from credit.infrastructure.daos.credit_payment_dao import CreditPaymentDAO

from currency_rates.models import CurrencyAccount, Currency
from user.models import User


class TestCreditPaymentDAO(TestCase):
    def setUp(self):
        self.dao = CreditPaymentDAO()
        self.currency = Currency.objects.create(name=constants.currency.CURRENCY_CODE_USD)
        self.credit_config = CreditConfiguration.objects.create(
            amount=Decimal('5000.00'),
            interest_rate=Decimal('3.5'),
            term_months=12,
            currency=self.currency,
            name='Test Credit'
        )
        self.user = User.objects.create(name='Nicko', phone_number='+375111111111', password='Kk12345678')
        self.currency_account = CurrencyAccount.objects.create(
            currency=self.currency,
            user=self.user,
            balance=1000,
        )

        self.credit = Credit.objects.create(
            currency_account=self.currency_account,
            configuration=self.credit_config,
            monthly_payment=Decimal('450.00'),
            remaining_amount=Decimal('5000.00'),
            closed=False
        )

    def test_orm_to_entity(self):
        entity = self.dao._orm_to_entity(self.credit, Decimal('1000.00'))
        assert isinstance(entity, CreditPaymentEntity)
        assert entity.credit_pk == self.credit.pk
        assert entity.amount == self.credit.remaining_amount
        assert entity.interest_rate == 100 * self.credit.configuration.interest_rate
        assert entity.term_month == self.credit.configuration.term_months
        assert entity.currency == self.credit.configuration.currency.name
        assert entity.available_cash == Decimal('1000.00')
        assert entity.monthly_payment == self.credit.monthly_payment

    def test_fetch_by_credit_pk(self):
        entity = self.dao.fetch_by_credit_pk(self.credit.pk)
        assert isinstance(entity, CreditPaymentEntity)
        assert entity.credit_pk == self.credit.pk
        assert entity.amount == self.credit.remaining_amount
        assert entity.interest_rate == 100 * self.credit.configuration.interest_rate
        assert entity.term_month == self.credit.configuration.term_months
        assert entity.currency == self.credit.configuration.currency.name
        assert entity.available_cash == self.credit.currency_account.balance
        assert entity.monthly_payment == self.credit.monthly_payment

    def test_fetch_by_phone_number(self):
        entities = self.dao.fetch_by_phone_number('1234567890')
        assert isinstance(entities, list)
        assert all(isinstance(entity, CreditPaymentEntity) for entity in entities)

        for entity in entities:
            credit = Credit.objects.get(pk=entity.credit_pk)
            currency_account = CurrencyAccount.objects.get(
                user=credit.currency_account.user,
                currency__name=credit.configuration.currency.name
            )

            assert entity.credit_pk == credit.pk
            assert entity.amount == credit.remaining_amount
            assert entity.interest_rate == 100 * credit.configuration.interest_rate
            assert entity.term_month == credit.configuration.term_months
            assert entity.currency == credit.configuration.currency.name
            assert entity.available_cash == currency_account.balance
            assert entity.monthly_payment == credit.monthly_payment
