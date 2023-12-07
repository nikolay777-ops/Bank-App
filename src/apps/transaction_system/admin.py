from django.contrib import admin
from django import forms

from transaction_system.models import Transaction


class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


@admin.register(Transaction)
class TransactionViewAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
