from django.core.cache import cache

from django.shortcuts import render, redirect
from .models import Transaction
from account_system.infrastructure.services.user_check_in_session import user_check_in_session
from account_system.models import User

def transaction_history(request):
    user = user_check_in_session(request, cache)
    if user:
        request.session['user_id'] = user.id
        transactions = Transaction.objects.filter(recipient_id=user.id, corespondent_id=user.id)
        for transaction in transactions:
            recipient = User.objects.get(id=transaction.recipient)
            corespondent = User.objects.get(id=transaction.corespondent)
            transaction.recipient_name = recipient.name
            transaction.corespondent_name = corespondent.name
        return render(request, 'transaction_system/transaction_history.html',
                      {'transactions': transactions, 'user_id': user.id})
    else:
        return render(request, 'transaction_system/transaction_history.html')
