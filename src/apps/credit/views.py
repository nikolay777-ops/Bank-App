from django.shortcuts import render, redirect
from django.core.cache import cache
from django.db.models import Q

from user.models import User
from currency_rates.models import CurrencyAccount
from credit.models.credit import Credit
from credit.models.credit_config import CreditConfiguration


def credit_configuration_list(request):
    user_name = cache.get('user_name')
    secret_key = cache.get(f"2fa_secret_key_{user_name}")
    phone_num = cache.get(f'phone_num')
    user = User.objects.get(phone_number=phone_num)

    if user_name and secret_key:
        if request.method == 'GET':
            user_credits = Credit.objects.only('configuration').filter(user__phone_number=phone_num)
            credit_configs = CreditConfiguration.objects.exclude(pk__in=user_credits.values_list('pk', flat=True))
            return render(
                request,
                'credit_system/credit_list.html',
                {'credit_configurations': credit_configs, 'user': user}
            )
        elif request.method == 'POST':
            credit_config_id = request.POST.get('credit_configuration_id')
            if user:
                credit_config = CreditConfiguration.objects.get(id=credit_config_id)
                account = CurrencyAccount.objects.get(user_id=user.pk, currency_id=credit_config.currency.name)
                remaining_amount = credit_config.amount * (1 + credit_config.interest_rate)

                credit = Credit.objects.create(
                    user=user,
                    configuration=credit_config,
                    remaining_amount=remaining_amount,
                    monthly_payment=remaining_amount / credit_config.term_months
                )

                credit.save()
                account.amount += credit_config.amount
                account.save()

                return redirect('account_list', currency=account.currency.name)

    return redirect('login')
