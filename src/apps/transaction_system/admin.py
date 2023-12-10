from django.contrib import admin
from django import forms

from transaction_system.models import Transaction
from account_system.models import User, Currency


class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].queryset = Currency.objects.all()
        self.fields['recipient_id'].queryset = User.objects.all()
        self.fields['corespondent_id'].queryset = User.objects.all()


@admin.register(Transaction)
class TransactionViewAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
