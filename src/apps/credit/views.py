from decimal import Decimal

from django.shortcuts import render, redirect

from credit.infrastructure.daos.credit_pay_dao import CreditPayDAO
from user.models import User
from currency_rates.models import CurrencyAccount
from credit.models.credit import Credit
from credit.models.credit_config import CreditConfiguration


def credit_configuration_list(request):
    if request.method == 'GET':
        phone_num = request.user.phone_number
        user_credits = Credit.objects.only('configuration').filter(user__phone_number=phone_num)
        credit_configs = CreditConfiguration.objects.exclude(pk__in=user_credits.values_list('pk', flat=True))
        return render(
            request,
            'credit_system/credit_list.html',
            {'credit_configurations': credit_configs}
        )

    elif request.method == 'POST':
        credit_config_id = request.POST.get('credit_configuration_id')
        if isinstance(request.user, User):
            credit_config = CreditConfiguration.objects.get(id=credit_config_id)
            account = CurrencyAccount.objects.get(user_id=request.user.pk, currency_id=credit_config.currency.name)
            real_interest_rate = Decimal(credit_config.interest_rate * Decimal(credit_config.term_months / 12))
            remaining_amount = credit_config.amount * (1 + real_interest_rate)

            credit = Credit.objects.create(
                user=request.user,
                configuration=credit_config,
                remaining_amount=remaining_amount,
                monthly_payment=remaining_amount / credit_config.term_months
            )

            credit.save()
            account.balance += credit_config.amount
            account.save()

            return redirect('account_list', currency=account.currency.name)

    return redirect('login')


def user_credit_list(request):
    if request.method == 'GET':
        phone_number = request.user.phone_number
        dao = CreditPayDAO()
        credit_pay_entity_list = dao.fetch_by_phone_number(phone_num=phone_number)
        context = {
            'entities': credit_pay_entity_list,
        }

        return render(request, 'credit_system/my_credits.html', context)

    elif request.method == 'POST':
        return redirect('home')

    return redirect('login')
