from django.db.models import Max
from django.shortcuts import render, redirect

from stocks.models import StockPrices, InvestmentPortfolio
from user.models import User


def list_stock(request):
    if request.method == "GET":
        latest_stocks = StockPrices.objects.values('stock__name').annotate(latest_timestamp=Max('date_of_use'))

        # Query the stocks again to get the prices at those timestamps
        latest_prices = StockPrices.objects.filter(
            date_of_use__in=[stock['latest_timestamp'] for stock in latest_stocks],
            stock__name__in=[stock['stock__name'] for stock in latest_stocks]
        )

        portfolios = None
        if isinstance(request.user, User):
            portfolios = InvestmentPortfolio.objects.filter(owner=request.user)

        context = {
            'stock_prices': latest_prices,
            'portfolios': portfolios
        }

        return render(request, 'stocks/stock_list.html', context)

    elif request.method == "POST":
        return redirect('home')
