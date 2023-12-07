from django.contrib import admin
from django import forms

from payments.models import Payment, PaymentTransaction
from user.models import User


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


class PaymentTransactionAdminForm(forms.ModelForm):
    class Meta:
        model = PaymentTransaction
        fields = ('payment', 'sender', 'count')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender'].queryset = User.objects.all()


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    form = PaymentTransactionAdminForm
    fields = ('payment', 'sender', 'count', 'created_at')
