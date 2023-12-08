from django.contrib import admin
from django import forms

from stocks.models import InvestmentPortfolio, InvestmentStrategy, Stock, StockPrices, StockTransaction, Subscriber
from user.models import User


class InvestmentPortfolioAdminForm(forms.ModelForm):
    class Meta:
        model = InvestmentPortfolio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.all()


@admin.register(InvestmentPortfolio)
class InvestmentPortfolioAdmin(admin.ModelAdmin):
    def owner_name(self, obj):
        return obj.owner.name

    form = InvestmentPortfolioAdminForm
    fields = ('owner', 'name')
    list_display = (
        'pk',
        'owner_name',
        'name'
    )


class InvestmentStrategyAdminForm(forms.ModelForm):
    class Meta:
        model = InvestmentStrategy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['investment_portfolio'].queryset = User.objects.all()


@admin.register(InvestmentStrategy)
class InvestmentStrategyAdmin(admin.ModelAdmin):
    form = InvestmentStrategyAdminForm
    fields = ('owner', 'name')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


class StockPricesAdminForm(forms.ModelForm):
    class Meta:
        model = StockPrices
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.all()


@admin.register(StockPrices)
class StockAdmin(admin.ModelAdmin):
    form = StockPricesAdminForm
    ordering = ('-date_of_use', )
    list_filter = ('stock', 'rate', 'date_of_use')
    list_display = ('stock', 'rate', 'date_of_use')

    fieldsets = (
        (
            'Main', {
                'fields': (
                    'stock',
                    'rate',
                    'date_of_use'
                )
            }
        ),
    )


class StockTransactionAdminForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inv_portfolio'].queryset = InvestmentPortfolio.objects.all()
        self.fields['stock_price'].queryset = StockPrices.objects.all()


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    def stock_name(self, obj):
        return obj.stock_price.stock.name

    def stock_price_value(self, obj):
        return obj.stock_price.rate

    def stock_price_datetime(self, obj):
        return obj.stock_price.date_of_use

    def owner(self, obj):
        return obj.inv_portfolio.owner.name

    def inv_port_name(self, obj):
        return obj.inv_portfolio.name

    stock_name.short_description = 'Stock Name'
    stock_price_value.short_description = 'Stock Price'
    owner.short_description = 'Owner Name'
    inv_port_name.short_description = 'Portfolio Name'

    list_display = (
        'owner',
        'inv_port_name',
        'stock_name',
        'stock_price_datetime',
        'stock_price_value',
        'count',
        'buy'
    )

    list_filter = (
        'inv_portfolio__owner',
        'inv_portfolio__name',
        'stock_price__stock__name',
    )

    form = StockTransactionAdminForm
    fields = ('inv_portfolio', 'stock_price', 'count', 'buy')


class SubscriberAdminForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
        self.fields['strategy'].queryset = InvestmentStrategy.objects.all()


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    form = SubscriberAdminForm
    fields = ('user', 'strategy')
