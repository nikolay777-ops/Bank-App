from django.contrib import admin
from django import forms

from credit_system.models import CreditRequest, CreditPayment, GeneralConfig


class CreditRequestAdminForm(forms.ModelForm):
    class Meta:
        model = CreditRequest
        fields = '__all__'


@admin.register(CreditRequest)
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
        model = GeneralConfig
        fields = '__all__'


@admin.register(GeneralConfig)
class CreditRequestViewAdmin(admin.ModelAdmin):
    form = GeneralConfigAdminForm