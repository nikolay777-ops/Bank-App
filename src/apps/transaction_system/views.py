from decimal import Decimal

from django.shortcuts import render, redirect
from .models import Transaction
from account_system.models import User
from django.db.models import Q
from transaction_system.infrastructure.services.transaction_processor import TransactionProcessor, TransactionEntity
from account_system.models import Account, Currency


def transaction_history(request):
    user = request.user
    if isinstance(user, User):
        transactions = list(reversed(list(Transaction.objects.filter(Q(recipient_id=user.id) |
                                                                     Q(corespondent_id=user.id) &
                                                                     Q(success=True)))))
        for transaction in transactions:
            transaction.recipient_name = transaction.recipient_id.name
            transaction.corespondent_name = transaction.corespondent_id.name
            transaction.recipient_id_id = transaction.recipient_id.id
        return render(request, 'transaction_system/transaction_history.html',
                      {'transactions': transactions, 'user_id': user.id})
    else:
        return redirect('home')

def create_transaction(request):
    user = request.user
    if isinstance(user, User):
        if request.method == 'POST':

            phone_number = request.POST['phone_number']
            amount = request.POST['amount']
            currency = request.POST['currency']

            # Phone number validation
            if not phone_number.startswith('+375') or len(phone_number) != 13:
                currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
                error_message = 'Phone number must start with +375 and have 13 digits.'
                return render(request, 'transaction_system/create_transaction.html',
                              {'currencies': currencies,
                               'user_id': user.id,
                               'error_message': error_message})

            # Amount validation
            try:
                amount = Decimal(amount)
            except:
                currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
                error_message = 'Transfer amount must be a float'
                return render(request, 'transaction_system/create_transaction.html',
                              {'currencies': currencies,
                               'user_id': user.id,
                               'error_message': error_message})
            if amount <= 0:
                currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
                error_message = 'Transfer amount must be a number greater than 0.'
                return render(request, 'transaction_system/create_transaction.html',
                              {'currencies': currencies,
                               'user_id': user.id,
                               'error_message': error_message})

            try:
                recipient = User.objects.get(Q(phone_number=phone_number) & ~Q(pk=user.id))
                recipient_currencies = list(Account.objects.filter(Q(owner=recipient.pk)).values_list('currency', flat=True))
                if not(currency in recipient_currencies):
                    currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
                    error_message = 'The recipient does not have an account in this currency'
                    return render(request, 'transaction_system/create_transaction.html',
                                  {'currencies': currencies,
                                   'user_id': user.id,
                                   'error_message': error_message})
            except User.DoesNotExist:
                currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
                error_message = 'User with such a phone number does not exist.'
                return render(request, 'transaction_system/create_transaction.html',
                              {'currencies': currencies,
                               'user_id': user.id,
                               'error_message': error_message})

            transaction_processor = TransactionProcessor()
            entity = TransactionEntity(
                pk=-1,
                currency_pk=currency,
                recipient_pk=recipient,
                corespondent_pk=user,
                amount=amount,
            )
            transaction_processor.create_transaction(entity)
            return redirect('home')
        else:
            currencies = list(Account.objects.filter(Q(owner=user.id)).values_list('currency', flat=True))
            return render(request, 'transaction_system/create_transaction.html',
                          {'currencies': currencies,
                           'user_id': user.id})
    else:
        return redirect('home')