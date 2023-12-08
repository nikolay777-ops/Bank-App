from abc import ABC

from django.db.models import Sum, Avg, Max, OuterRef, Subquery

from stocks.domain.entities import InvestmentPortfolioEntity, StockEntity
from stocks.domain.interfaces import IInvestmentPortfolioDAO
from stocks.models import StockTransaction, StockPrices
from stocks.models.investment_portfolio import InvestmentPortfolio


class InvestmentPortfolioDAO(IInvestmentPortfolioDAO, ABC):
    def fetch_by_user_pk(
            self,
            user_pk: int
    ) -> list[InvestmentPortfolioEntity]:
        portfolio_pk_list = InvestmentPortfolio.objects.values('pk').get(owner_id=user_pk).values()

        investment_portfolio_entity_list = [
            self.fetch_by_portfolio_pk(portfolio_pk=pk)
            for pk in portfolio_pk_list
        ]

        return investment_portfolio_entity_list

    def fetch_by_portfolio_pk(
            self,
            portfolio_pk: int
    ) -> InvestmentPortfolioEntity:
        portfolio = InvestmentPortfolio.objects.only('owner_id', 'name').get(pk=portfolio_pk)

        # Get all StockTransaction instances where buy is True and related to the given portfolio
        transactions = StockTransaction.objects.filter(buy=True, inv_portfolio_id=portfolio_pk)

        latest_stock_prices = StockPrices.objects.filter(
            stock=OuterRef('stock_price__stock')
        ).order_by('-date_of_use')

        # Group by stock_prices and stock, and calculate the sum of count, average of stock_price, and latest date
        grouped_transactions = transactions.values('stock_price__stock__name').annotate(
            total_count=Sum('count'),
            average_price=Avg('stock_price__rate'),
            latest_date=Max('stock_price__date_of_use'),
            latest_rate=Subquery(latest_stock_prices.values('rate')[:1]),
        )

        # Create a list of StockEntity instances
        stocks = [
            StockEntity(
                name=transaction['stock_price__stock__name'],
                rate=transaction['average_price'],
                date_of_use=transaction['latest_date'],
                count=transaction['total_count'],
                profit=((transaction['latest_rate'] - transaction['average_price']) / transaction['average_price']) * 100,
            ) for transaction in grouped_transactions
        ]

        # Create an InvestmentPortfolioEntity instance
        portfolio_entity = InvestmentPortfolioEntity(
            owner_pk=portfolio.owner_id,
            name=portfolio.name,
            stocks=stocks
        )

        return portfolio_entity

