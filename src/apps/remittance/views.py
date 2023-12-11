from decimal import Decimal

from django.shortcuts import render, redirect

from currency_rates.models import CurrencyAccount
from .models.remittance import Remittance
from user.models.user import User
from django.db.models import Q
from remittance.infrastructure.services.remittance_processor import RemittanceProcessor, RemittanceEntity
from currency_rates.models.currency import Currency


def transaction_history(request):
    user = request.user
    if isinstance(user, User):
        transactions = list(
            reversed(list(Remittance.objects.filter(receiver_id=user.pk, sender_id=user.pk, success=True))))
        for transaction in transactions:
            transaction.reciever = transaction.recipient_id.name
            transaction.corespondent_name = transaction.corespondent_id.name
            transaction.recipient_id_id = transaction.recipient_id.id
        return render(request, 'remittance/history_remittance.html',
                      {'transactions': transactions, 'user_id': user.pk})
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
                currencies = list(CurrencyAccount.objects.filter(user=user.pk).values_list('currency', flat=True))
                error_message = 'Phone number must start with +375 and have 13 digits.'
                return render(request, 'remittance/create_remittance.html',
                              {'currencies': currencies,
                               'user_id': user.pk,
                               'error_message': error_message})

            # Amount validation
            try:
                amount = Decimal(amount)
            except:
                currencies = list(CurrencyAccount.objects.filter(user=user.pk).values_list('currency', flat=True))
                error_message = 'Transfer amount must be a float'
                return render(request, 'remittance/create_remittance.html',
                              {'currencies': currencies,
                               'user_id': user.pk,
                               'error_message': error_message})
            if amount <= 0:
                currencies = list(CurrencyAccount.objects.filter(user=user.pk).values_list('currency', flat=True))
                error_message = 'Transfer amount must be a number greater than 0.'
                return render(request, 'remittance/create_remittance.html',
                              {'currencies': currencies,
                               'user_id': user.pk,
                               'error_message': error_message})

            try:
                recipient = User.objects.get(phone_number=phone_number)
                recipient_currencies = list(
                    CurrencyAccount.objects.filter(user=recipient.pk).values_list('currency', flat=True))
                if not (currency in recipient_currencies):
                    currencies = list(
                        CurrencyAccount.objects.filter(Q(user=user.id)).values_list('currency', flat=True))
                    error_message = 'The recipient does not have an account in this currency'
                    return render(request, 'remittance/create_remittance.html',
                                  {'currencies': currencies,
                                   'user_id': user.pk,
                                   'error_message': error_message})
            except User.DoesNotExist:
                currencies = list(CurrencyAccount.objects.filter(user=user.pk).values_list('currency', flat=True))
                error_message = 'User with such a phone number does not exist.'
                return render(request, 'remittance/create_remittance.html',
                              {'currencies': currencies,
                               'user_id': user.pk,
                               'error_message': error_message})

            transaction_processor = RemittanceProcessor()
            entity = RemittanceEntity(
                pk=-1,
                currency_pk=currency,
                receiver_pk=recipient.pk,
                sender_pk=user.pk,
                count=amount,
            )
            transaction_processor.create_remittance(entity)
            return redirect('home')
        else:
            currencies = list(CurrencyAccount.objects.filter(user=user.pk).values_list('currency', flat=True))
            return render(request, 'remittance/create_remittance.html',
                          {'currencies': currencies,
                           'user_id': user.pk})
    else:
        return redirect('home')


def view_incoming_transactions(request):
    user = request.user
    if isinstance(user, User):
        if request.method == 'POST':
            transaction_id = request.POST.get('transaction_id')
            transaction_processor = RemittanceProcessor()
            if transaction_processor.accept_remittance(transaction_id):
                return redirect('view_incoming_transactions')
            else:
                transactions = list(reversed(list(Remittance.objects.filter(Q(receiver_id=user.pk) &
                                                                            Q(accepted=False)))))
                for transaction in transactions:
                    transaction.recipient_name = transaction.recipient_id.name
                    transaction.corespondent_name = transaction.corespondent_id.name
                    transaction.recipient_id_id = transaction.recipient_id.id
                return render(request, 'remittance/view_incoming_transactions.html',
                              {'transactions': transactions, 'user_id': user.pk,
                               'error_message': 'The corespondent does not have enough funds in the account'})
        else:
            transactions = list(reversed(list(Remittance.objects.filter(Q(receiver_id=user.id) &
                                                                        Q(accepted=False)))))
            for transaction in transactions:
                transaction.recipient_name = transaction.receiver.name
                transaction.corespondent_name = transaction.sender.name
                transaction.recipient_id_id = transaction.receiver.id
            return render(request, 'remittance/view_incoming_transactions.html',
                          {'transactions': transactions, 'user_id': user.pk})
    else:
        return redirect('home')
