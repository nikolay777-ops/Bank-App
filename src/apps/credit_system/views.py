from decimal import Decimal

from django.shortcuts import render, redirect

from credit_system.infrastructure.daos.credit_payment_dao import CreditPaymentDAO
from credit_system.infrastructure.services.credit_payment_processor import CreditPaymentProcessor
from account_system.models import User, Account
from credit_system.models import Credit, CreditConfiguration


def credit_configuration_list(request):
    if isinstance(request.user, User):
        if request.method == 'GET':
            phone_num = request.user.phone_number
            user_credits = Credit.objects.only('configuration').filter(currency_account__owner__phone_number=phone_num, closed=False)
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
                account = Account.objects.get(owner_id=request.user.pk, currency_id=credit_config.currency.name)
                if len(Credit.objects.filter(
                        currency_account=account,
                        configuration=credit_config,
                        closed=False
                )) == 0:
                    real_interest_rate = Decimal(credit_config.interest_rate * Decimal(credit_config.term_months / 12))
                    remaining_amount = credit_config.amount * (1 + real_interest_rate)

                    credit = Credit.objects.create(
                        currency_account=account,
                        configuration=credit_config,
                        remaining_amount=remaining_amount,
                        monthly_payment=remaining_amount / credit_config.term_months
                    )

                    credit.save()
                    account.amount += credit_config.amount
                    account.save()

                    return redirect('account_list', currency=account.currency.name)

                else:
                    phone_num = request.user.phone_number
                    user_credits = Credit.objects.only('configuration').filter(
                        currency_account__owner__phone_number=phone_num, closed=False)
                    credit_configs = CreditConfiguration.objects.exclude(pk__in=user_credits.values_list('pk', flat=True))

                    context = {
                        'credit_configurations': credit_configs,
                        'credit_not_closed': "You already have that credit and it's unpaid"
                    }

                    return render(
                        request,
                        'credit_system/credit_list.html',
                        context
                    )

    return redirect('login')


def user_credit_list(request):
    if isinstance(request.user, User):
        if request.method == 'GET':
            phone_number = request.user.phone_number
            dao = CreditPaymentDAO()
            credit_pay_entity_list = dao.fetch_by_phone_number(phone_num=phone_number)
            context = {
                'entities': credit_pay_entity_list,
            }

            return render(request, 'credit_system/my_credits.html', context)

        elif request.method == 'POST':
            credit_payment_processor = CreditPaymentProcessor()
            payment_entity = CreditPaymentDAO().fetch_by_credit_pk(
                request.POST['credit_pk']
            )

            credit_payment_processor.create_credit_payment(
                payment_entity=payment_entity,
                amount=Decimal(request.POST['amount'])
            )

            return redirect('user_credit_list')

    return redirect('login')