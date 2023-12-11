from django.shortcuts import render, redirect
from transaction_system.models import Transaction
from account_system.models import User, Account
from django.db.models import Q

from django.db.models import Avg, Sum
from django.utils import timezone
from datetime import timedelta


def statistics_view(request):
    user = request.user
    if isinstance(user, User):
        # Получаем текущую дату и время и вычитаем из нее месяц и год
        current_datetime = timezone.now()
        last_month_datetime = current_datetime - timedelta(days=30)
        last_year_datetime = current_datetime - timedelta(days=365)
        currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
        stats = []
        for currency in currencies:
            # Вычисляем средний чек за последний месяц
            result = Transaction.objects.filter(
                Q(timestamp__gte=last_month_datetime) &
                Q(corespondent_id=user.id) &
                Q(success=True) &
                Q(currency=currency)
            ).aggregate(Avg('amount'))['amount__avg']

            if result is not None:
                average_amount_last_month = round(result, 2)
            else:
                average_amount_last_month = 0.00

            income_last_month = Transaction.objects.filter(
                Q(timestamp__gte=last_month_datetime) &
                Q(recipient_id=user.id) &
                Q(success=True) &
                Q(currency=currency)
            )

            # Вычисляем средний доход за последний месяц
            if income_last_month is not None:
                a_income_last_month = income_last_month.aggregate(Sum('amount'))['amount__sum']
                if a_income_last_month is not None:
                    average_income_last_month = round(
                        income_last_month.aggregate(Sum('amount'))['amount__sum'] / income_last_month.count(), 2)
                else:
                    average_income_last_month = 0.00
                if income_last_month.count() == 1:
                    index = 0
                else:
                    index = int(income_last_month.count() / 2)
                my_list = list(income_last_month.values_list('amount', flat=True))
                if my_list is not None and index is not None:
                    # Вычисляем медианный доход за последний месяц
                    median_income_last_month = round(my_list[index], 2)
                else:
                    median_income_last_month = 0.00
            else:
                average_income_last_month = 0.00
                median_income_last_month = 0.00

            # Вычисляем средний доход за последний год
            income_last_year = Transaction.objects.filter(
                Q(timestamp__gte=last_year_datetime) &
                Q(recipient_id=user.id) &
                Q(success=True) &
                Q(currency=currency)
            )
            if income_last_year is not None \
                    and income_last_year.aggregate(Sum('amount'))['amount__sum'] is not None:
                average_income_last_year = round(income_last_year.aggregate(Sum('amount'))['amount__sum'] / income_last_year.count(), 2)
            else:
                average_income_last_year = 0.00
            stat = {
                'average_amount_last_month': average_amount_last_month,
                'average_income_last_month': average_income_last_month,
                'median_income_last_month': median_income_last_month,
                'average_income_last_year': average_income_last_year,
                'currency': currency,
            }
            stats.append(stat)
        return render(request, 'stats_system/my_stat.html', {
            'stats': stats
        })
    else:
        return redirect('home')