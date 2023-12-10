from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.shortcuts import render, redirect

import constants.currency
from currency_rates.infrastructure.daos.currency_rates_dao import CurrencyRatesDAO
from currency_rates.models import CurrencyAccount, CurrencyRate
from stocks.forms import InvestmentPortfolioCreateForm
from stocks.infrastructure.daos.investment_portfolio_dao import InvestmentPortfolioDAO
from stocks.infrastructure.services.investment_portfolio_processor import InvestmentPortfolioProcessor
from stocks.models import StockPrices, InvestmentPortfolio, StockTransaction
from user.models import User


def prepare_stocks(user):
    latest_stocks = StockPrices.objects.values('stock__name').annotate(latest_timestamp=Max('date_of_use'))

    # Query the stocks again to get the prices at those timestamps
    latest_prices = StockPrices.objects.filter(
        date_of_use__in=[stock['latest_timestamp'] for stock in latest_stocks],
        stock__name__in=[stock['stock__name'] for stock in latest_stocks]
    )

    portfolios = None
    accounts = None
    if isinstance(user, User):
        portfolios = InvestmentPortfolio.objects.filter(owner=user)
        accounts = CurrencyAccount.objects.filter(user=user)

    context = {
        'stock_prices': latest_prices,
        'portfolios': portfolios,
        'accounts': accounts
    }

    return context


def list_stock(request):
    if request.method == "GET":
        context = prepare_stocks(request.user)
        return render(request, 'stocks/stock_list.html', context)

    elif request.method == "POST":
        try:
            account_currency = CurrencyAccount.objects.get(pk=request.POST['account'])

            currency_rate_dao = CurrencyRatesDAO()
            usd_rate = currency_rate_dao.fetch_latest_by_currency_pk(currency_pk=constants.currency.CURRENCY_CODE_USD)
            account_rate = currency_rate_dao.fetch_latest_by_currency_pk(currency_pk=account_currency.currency.name)
            amount = int(request.POST.get('amount_{}'.format(request.POST['stock_name'])))

            stock_sum = usd_rate.rate * amount * account_rate.rate * float(request.POST['stock_rate'])

            if stock_sum <= account_currency.balance:
                portfolio_pk = request.POST['portfolio']
                stock_price_pk = request.POST['stock_price_pk']

                account_currency.balance -= Decimal(stock_sum)
                StockTransaction.objects.create(
                    inv_portfolio_id=portfolio_pk,
                    stock_price_id=stock_price_pk,
                    count=amount,
                )
                account_currency.save()

                return redirect('home')

            else:
                errors = {
                    'error': 'You have enough money for buy that amount of stock'
                }
                context = prepare_stocks(request.user)
                context['errors'] = errors
                return render(request, 'stocks/stock_list.html', context)

        except ObjectDoesNotExist:
            errors = {
                'error': 'At this time you can not buy stocks'
            }
            context = {
                'errors': errors
            }
            return render(request, 'stocks/stock_list.html', context)


def investment_portfolio_view(request):
    if isinstance(request.user, User):
        if request.method == 'GET':
            dao = InvestmentPortfolioDAO()
            portfolios = dao.fetch_by_user_pk(request.user.pk)
            form = InvestmentPortfolioCreateForm()

            context = {
                'portfolios': portfolios,
                'form': form,
            }

            return render(request, 'stocks/investment_portfolio_list.html', context)

        if request.method == 'POST':
            if len(request.POST['portfolio_name']) == 0:
                dao = InvestmentPortfolioDAO()
                portfolios = dao.fetch_by_user_pk(request.user.pk)
                form = InvestmentPortfolioCreateForm()

                context = {
                    'portfolios': portfolios,
                    'form': form,
                }

                errors = {
                    'error': 'There is empty portfolio name'
                }
                context['errors'] = errors

                return render(request, 'stocks/investment_portfolio_list.html', context)

            InvestmentPortfolio.objects.create(
                owner=request.user,
                name=request.POST['portfolio_name']
            )

            return redirect('investment_portfolio_view')
    return redirect('login')


def sell_all_stocks_view(request):
    if isinstance(request.user, User):
        if request.method == 'POST':
            processor = InvestmentPortfolioProcessor()
            processor.sell_all_stocks(portfolio_name=request.POST['portfolio-name'], user_id=request.user.pk)

        return redirect('home')

    return redirect('login')
