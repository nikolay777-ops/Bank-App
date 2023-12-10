import constants.currency
from currency_rates.models import CurrencyAccount
from stocks.models import InvestmentPortfolio, StockTransaction, StockPrices
from user.models import User
from django.db.models import F


class InvestmentPortfolioProcessor:
    def sell_all_stocks(self, portfolio_name: int, user_id: int):
        buy_transactions = StockTransaction.objects.filter(
            buy=True,
            inv_portfolio__name=portfolio_name,
            inv_portfolio__owner_id=user_id
        )

        # Calculate the total amount from selling all stocks
        total_amount = 0
        for transaction in buy_transactions:
            # Get the latest stock price for the stock in the transaction
            latest_stock_price = StockPrices.objects.filter(stock=transaction.stock_price.stock).latest('date_of_use')

            # Calculate the amount for this transaction
            amount = transaction.count * latest_stock_price.rate

            # Add the amount to the total
            total_amount += amount

        # Add the total amount to the currency account with currency='USD'
        currency_account = CurrencyAccount.objects.get(currency__name=constants.currency.CURRENCY_CODE_USD, user_id=user_id)
        currency_account.balance = F('balance') + total_amount
        currency_account.save()

        InvestmentPortfolio.objects.filter(name=portfolio_name, owner_id=user_id).delete()
