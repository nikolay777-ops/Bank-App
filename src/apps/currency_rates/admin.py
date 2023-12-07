from django.contrib import admin
from django import forms

from currency_rates.models.currency import Currency
from currency_rates.models.currency_account import CurrencyAccount
from currency_rates.models.currency_rates import CurrencyRate
from currency_rates.models.currency_transaction import CurrencyTransaction
from user.admin import UserAdmin
from user.models import User


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


class CurrencyAccountAdminForm(forms.ModelForm):
    class Meta:
        model = CurrencyAccount
        fields = ('user', 'currency', 'balance')


@admin.register(CurrencyAccount)
class CurrencyAccountAdmin(admin.ModelAdmin):
    fields = ('user', 'currency', 'balance')
    form = CurrencyAccountAdminForm


class CurrencyRateAdminForm(forms.ModelForm):
    class Meta:
        model = CurrencyRate
        fields = ('currency', 'rate', 'date_of_use')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    form = CurrencyAccountAdminForm
    fields = ('currency', 'rate', 'date_of_use')


class CurrencyTransactionAdminForm(forms.ModelForm):
    class Meta:
        model = CurrencyTransaction
        fields = ('user', 'currency_rate', 'count')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
        self.fields['currency_rate'].queryset = CurrencyRate.objects.all()


@admin.register(CurrencyTransaction)
class CurrencyTransactionAdmin(admin.ModelAdmin):
    form = CurrencyTransactionAdminForm
    fields = ('user', 'currency_rate', 'count')
