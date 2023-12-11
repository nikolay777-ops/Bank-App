import pytest
from decimal import Decimal
from django.test import TestCase

import constants
from credit.models import CreditConfiguration
from credit.models.credit_payment import CreditPayment
from credit.models.credit import Credit
from credit.domain.entities import CreditPaymentEntity
from credit.infrastructure.services.credit_payment_processor import CreditPaymentProcessor
from currency_rates.models import CurrencyAccount, Currency
from user.models import User


class TestCreditPaymentProcessor(TestCase):
    def setUp(self):
        self.processor = CreditPaymentProcessor()
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
            monthly_payment=Decimal('416.67'),
            remaining_amount=Decimal('5000.00'),
            closed=False
        )
        self.payment_entity = CreditPaymentEntity(
            credit_pk=self.credit.pk,
            amount=self.credit.remaining_amount,
            interest_rate=100 * self.credit.configuration.interest_rate,
            term_month=self.credit.configuration.term_months,
            currency=self.credit.configuration.currency.name,
            available_cash=Decimal('1000.00'),
            monthly_payment=self.credit.monthly_payment
        )

    def test_count_monthly_payment(self):
        amount = Decimal('1000.00')
        monthly_payment = self.processor.count_montly_payment(self.payment_entity, amount)
        expected_monthly_payment = Decimal((self.payment_entity.amount - amount) / self.payment_entity.term_month)
        assert monthly_payment == expected_monthly_payment

    def test_create_credit_payment(self):
        amount = Decimal('1000.00')
        self.processor.create_credit_payment(self.payment_entity, amount)
        credit = Credit.objects.get(pk=self.payment_entity.credit_pk)
        assert credit.remaining_amount == self.payment_entity.amount - amount
        assert credit.currency_account.balance == self.payment_entity.available_cash - amount
        assert credit.monthly_payment == round(self.processor.count_montly_payment(self.payment_entity, amount), 2)
        assert credit.closed == (credit.remaining_amount == 0)
        credit_payment = CreditPayment.objects.get(credit=credit)
        assert credit_payment.amount == amount

    def test_create_credit_payment_full_amount(self):
        amount = self.payment_entity.amount  # Pay the full amount
        self.processor.create_credit_payment(self.payment_entity, amount)
        credit = Credit.objects.get(pk=self.payment_entity.credit_pk)
        assert credit.remaining_amount == 0
        assert credit.currency_account.balance == self.payment_entity.available_cash - amount
        assert credit.closed == True
        credit_payment = CreditPayment.objects.get(credit=credit)
        assert credit_payment.amount == amount

    def test_create_credit_payment_partial_amount(self):
        amount = self.payment_entity.amount / 2  # Pay half the amount
        self.processor.create_credit_payment(self.payment_entity, amount)
        credit = Credit.objects.get(pk=self.payment_entity.credit_pk)
        assert credit.remaining_amount == self.payment_entity.amount - amount
        assert credit.currency_account.balance == self.payment_entity.available_cash - amount
        assert credit.monthly_payment == round(self.processor.count_montly_payment(self.payment_entity, amount), 2)
        assert credit.closed == False
        credit_payment = CreditPayment.objects.get(credit=credit)
        assert credit_payment.amount == amount

    def test_create_credit_payment_zero_amount(self):
        amount = Decimal('0.00')  # Pay zero amount
        self.processor.create_credit_payment(self.payment_entity, amount)
        credit = Credit.objects.get(pk=self.payment_entity.credit_pk)
        assert credit.remaining_amount == self.payment_entity.amount
        assert credit.currency_account.balance == self.payment_entity.available_cash
        assert credit.monthly_payment == self.payment_entity.monthly_payment
        assert credit.closed == False
        credit_payment = CreditPayment.objects.get(credit=credit)
        assert credit_payment.amount == amount
