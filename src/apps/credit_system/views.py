from django.shortcuts import render, redirect
from django.core.cache import cache
from django.db.models import Q

from account_system.models import User, Account
from credit_system.models.credit import Credit
from credit_system.models.credit_config import CreditConfiguration


def credit_configuration_list(request):
    user_name = cache.get('user_name')
    secret_key = cache.get(f"2fa_secret_key_{user_name}")
    phone_num = cache.get(f'phone_num')

    if user_name and secret_key:
        if request.method == 'GET':
            credit_configs = Credit.objects.only('configuration').filter(~Q(user__phone_number=phone_num))
            return render(
                request,
                'credit_system/credit_list.html',
                {'credit_configurations': credit_configs}
            )
        elif request.method == 'POST':
            credit_config_id = request.POST.get('credit_configuration_id')
            user = User.objects.get(phone_number=phone_num)
            if user:
                credit_config = CreditConfiguration.objects.get(id=credit_config_id)
                account = Account.objects.get(owner_id=user.pk, currency_id=credit_config.currency.name)
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
