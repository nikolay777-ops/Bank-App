from decimal import Decimal

from django.db.models.functions import datetime
from django.shortcuts import redirect
from transaction_system.models import Transaction, LoyaltyConfig
from account_system.models import Account, User, Role, Currency
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta

def loyalty_program(request):
    user = request.user
    if isinstance(user, User):
        bank_role = Role.objects.get(name="Bank")
        bank = User.objects.get(role_id=bank_role)

        current_datetime = timezone.now()
        last_month_datetime = current_datetime - timedelta(days=30)
        currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
        account_moneys = list(Account.objects.filter(Q(owner=user.id)).values_list('amount', flat=True))
        for currency, account_money in zip(currencies, account_moneys):
            if not Transaction.objects.filter(Q(recipient_id=user.id) &
                                              Q(corespondent_id=bank) &
                                              Q(currency=currency)).exists():
                temp_money = account_money
                min = temp_money
                transactions = list(Transaction.objects.filter(
                    Q(timestamp__gte=last_month_datetime) &
                    (Q(recipient_id=user.id) | Q(corespondent_id=user.id)) &
                    Q(success=True) &
                    Q(currency=currency)
                ).values_list('amount', 'recipient_id'))

                for transaction in transactions:
                    if transaction[1] == user.id:
                        temp_money = temp_money + transaction[0]
                    else:
                        temp_money = temp_money - transaction[0]
                        if temp_money < min:
                            min = temp_money
                curr = Currency.objects.get(name=currency)
                if min > 0.00:
                    configs = list(reversed(list(LoyaltyConfig.objects.all().values_list('min', 'percent'))))
                    percent = Decimal(0.05)
                    for config in configs:
                        if min > config[0]:
                            percent = config[1]
                            break
                    Transaction.objects.create(
                        amount=round(min * percent, 2),
                        recipient_id=user,
                        corespondent_id=bank,
                        currency=curr,
                        timestamp=datetime.Now(),
                        commission=0.00,
                        success=True,
                        accepted=True,
                    )
    else:
        return redirect('home')
