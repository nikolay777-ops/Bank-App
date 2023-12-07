from django.contrib import admin
from django import forms

from currency_rates.models import Currency
from remittance.models.remittance import Remittance
from user.models import User


class RemittanceAdminForm(forms.ModelForm):
    class Meta:
        model = Remittance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].queryset = Currency.objects.all()
        self.fields['sender'].queryset = User.objects.all()
        self.fields['receiver'].queryset = User.objects.all()


@admin.register(Remittance)
class RemittanceAdmin(admin.ModelAdmin):
    form = RemittanceAdminForm
    fields = ('sender', 'receiver', 'currency', 'count', 'commission', 'success', 'accepted')
