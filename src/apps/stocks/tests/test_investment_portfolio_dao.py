import datetime

from django.test import TestCase

import constants.stocks
from stocks.models.investment_portfolio import InvestmentPortfolio
from stocks.models.stock_transaction import StockTransaction
from stocks.models.stock_prices import StockPrices
from stocks.models.stock import Stock
from stocks.domain.entities import InvestmentPortfolioEntity
from stocks.infrastructure.daos.investment_portfolio_dao import InvestmentPortfolioDAO
from user.models import User
from django.utils import timezone

class TestInvestmentPortfolioDAO(TestCase):
    def setUp(self):
        self.dao = InvestmentPortfolioDAO()
        self.user = User.objects.create(name='Nicko', phone_number='+375111111111', password='Kk12345678')
        self.stock = Stock.objects.create(
            name=constants.stocks.APPLE_STOCK_CODE,
        )
        self.stock_price = StockPrices.objects.create(
            stock=self.stock,
            rate=174,
            date_of_use=timezone.now()
        )
        self.portfolio = InvestmentPortfolio.objects.create(
            owner=self.user,
            name='Bablo'
        )
        self.transaction = StockTransaction.objects.create(
            inv_portfolio=self.portfolio,
            stock_price=self.stock_price,
            count=5,
            buy=True
        )

    def test_fetch_by_user_pk(self):
        entities = self.dao.fetch_by_user_pk(self.portfolio.owner.pk)
        assert isinstance(entities, list)
        assert all(isinstance(entity, InvestmentPortfolioEntity) for entity in entities)

        for entity in entities:
            portfolio = InvestmentPortfolio.objects.get(pk=entity.owner_pk)
            assert entity.owner_pk == portfolio.owner.pk
            assert entity.name == portfolio.name
            assert len(entity.stocks) == StockTransaction.objects.filter(inv_portfolio=portfolio).count()

            for stock_entity in entity.stocks:
                transaction = StockTransaction.objects.get(inv_portfolio=portfolio,
                                                           stock_price__stock__name=stock_entity.name)
                assert stock_entity.name == transaction.stock_price.stock.name
                assert stock_entity.rate == transaction.stock_price.rate
                assert stock_entity.date_of_use == transaction.stock_price.date_of_use
                assert stock_entity.count == transaction.count

    def test_fetch_by_portfolio_pk(self):
        entity = self.dao.fetch_by_portfolio_pk(self.portfolio.pk)
        assert isinstance(entity, InvestmentPortfolioEntity)
        assert entity.owner_pk == self.portfolio.owner.pk
        assert entity.name == self.portfolio.name
        assert len(entity.stocks) == 1
        stock_entity = entity.stocks[0]
        assert stock_entity.name == self.stock.name
        assert stock_entity.rate == self.stock_price.rate
        assert stock_entity.date_of_use == self.stock_price.date_of_use
        assert stock_entity.count == self.transaction.count

    def test_fetch_by_user_pk_multiple_transactions(self):
        # Create additional transactions for the same stock
        StockTransaction.objects.create(inv_portfolio=self.portfolio, stock_price=self.stock_price, count=5)
        StockTransaction.objects.create(inv_portfolio=self.portfolio, stock_price=self.stock_price, count=10)

        entities = self.dao.fetch_by_user_pk(self.portfolio.owner.pk)
        assert isinstance(entities, list)
        assert all(isinstance(entity, InvestmentPortfolioEntity) for entity in entities)

        for entity in entities:
            assert entity.owner_pk == self.portfolio.owner.pk
            assert entity.name == self.portfolio.name
            assert len(entity.stocks) == 1  # There should still be only one stock

            for stock_entity in entity.stocks:
                assert stock_entity.name == self.stock.name
                assert stock_entity.rate == self.stock_price.rate
                assert stock_entity.date_of_use == self.stock_price.date_of_use
                assert stock_entity.count == 20  # The count should now be 20

    def test_fetch_by_user_pk_no_transactions(self):
        # Delete all transactions
        StockTransaction.objects.all().delete()

        entities = self.dao.fetch_by_user_pk(self.portfolio.owner.pk)
        assert isinstance(entities, list)
        assert all(isinstance(entity, InvestmentPortfolioEntity) for entity in entities)

        for entity in entities:
            assert entity.owner_pk == self.portfolio.owner.pk
            assert entity.name == self.portfolio.name
            assert len(entity.stocks) == 0  # There should be no stocks
