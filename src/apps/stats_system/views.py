from django.shortcuts import render, redirect
from transaction_system.models import Transaction
from account_system.models import User
from django.db.models import Q

from django.db.models import Avg, Sum, Count
from django.utils import timezone
from datetime import timedelta


def statistics_view(request):
    user = request.user
    if isinstance(user, User):
        # Получаем текущую дату и время и вычитаем из нее месяц и год
        current_datetime = timezone.now()
        last_month_datetime = current_datetime - timedelta(days=30)
        last_year_datetime = current_datetime - timedelta(days=365)

        # Вычисляем средний чек за последний месяц
        result = Transaction.objects.filter(
            Q(timestamp__gte=last_month_datetime) &
            Q(corespondent_id=user.id) &
            Q(success=True)
        ).aggregate(Avg('amount'))['amount__avg']

        average_amount_last_month = round(result, 2)

        income_last_month = Transaction.objects.filter(
            Q(timestamp__gte=last_month_datetime) &
            Q(recipient_id=user.id) &
            Q(success=True)
        )

        # Вычисляем средний доход за последний месяц
        average_income_last_month = income_last_month.aggregate(Sum('amount'))['amount__sum']
        index = int(income_last_month.count() / 2)
        my_list = list(income_last_month.values_list('amount', flat=True))
        # Вычисляем медианный доход за последний месяц
        median_income_last_month = my_list[index]

        # Вычисляем средний доход за последний год
        average_income_last_year = Transaction.objects.filter(
            Q(timestamp__gte=last_year_datetime) &
            Q(recipient_id=user.id) &
            Q(success=True)
        ).aggregate(Sum('amount'))['amount__sum']
        return render(request, 'stats_system/my_stat.html', {
            'average_amount_last_month': average_amount_last_month,
            'average_income_last_month': average_income_last_month,
            'median_income_last_month': median_income_last_month,
            'average_income_last_year': average_income_last_year
        })
    else:
        redirect('home')