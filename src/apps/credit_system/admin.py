from django.contrib import admin
from django import forms

from account_system.models import Currency
from credit_system.models import Credit, CreditPayment, CreditConfiguration


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

class CreditRequestAdminForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'


@admin.register(Credit)
class CreditRequestViewAdmin(admin.ModelAdmin):
    form = CreditRequestAdminForm


class CreditPaymentAdminForm(forms.ModelForm):
    class Meta:
        model = CreditPayment
        fields = '__all__'


@admin.register(CreditPayment)
class CreditPaymentViewAdmin(admin.ModelAdmin):
    form = CreditPaymentAdminForm


class GeneralConfigAdminForm(forms.ModelForm):
    class Meta:
        model = CreditConfiguration
        fields = '__all__'


@admin.register(CreditConfiguration)
class CreditRequestViewAdmin(admin.ModelAdmin):
    form = GeneralConfigAdminForm