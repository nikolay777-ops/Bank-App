from django.core.cache import cache

from django.shortcuts import render, redirect
from .models import Transaction
from account_system.infrastructure.services.user_check_in_session import user_check_in_session
from account_system.models import User
from django.db.models import Q

def transaction_history(request):
    phone_num = cache.get('phone_num')
    user = User.objects.get(phone_number=phone_num)
    if user:
        request.session['user_id'] = user.id
        transactions = list(Transaction.objects.filter(Q(recipient_id=user.id) | Q(corespondent_id=user.id)))
        for transaction in transactions:
            transaction.recipient_name = transaction.recipient_id.name
            transaction.corespondent_name = transaction.corespondent_id.name
            transaction.recipient_id_id = transaction.recipient_id.id
        return render(request, 'transaction_system/transaction_history.html',
                      {'transactions': transactions, 'user_id': user.id})
    else:
        return render(request, 'transaction_system/transaction_history.html')
