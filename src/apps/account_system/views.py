import base64
import random
from decimal import Decimal
from io import BytesIO

from django.shortcuts import render, redirect

from account_system.models import Account, Role, Currency
from .forms import RegistrationForm, LoginForm
from .models import User
from account_system.infrastructure.services.two_factor_auth import generate_secret_key, generate_qr_code, verify_otp
from django.core.cache import cache
from transaction_system.infrastructure.services.loyalty_program import loyalty_program

from django.contrib.auth import login, authenticate, logout
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохранение формы, но не коммитить в базу данных
            role = Role.objects.get(name="user")
            user.role_id = role
            secret_key = generate_secret_key()
            user.secret_code = secret_key
            user.save()

            # cache user-secret code
            cache.set(f'user_name', user.name, 300)
            cache.set(f"2fa_secret_key_{user.name}", secret_key, 300)
            cache.set(f'phone_num', user.phone_number, 300)

            return redirect('two_factor_auth_qrcode')

        else:
            context = {
                'form': form,
                'errors': form.errors
            }
            return render(request, 'account_system/registration.html', context)
    else:
        context = {
            'form': RegistrationForm()
        }
        return render(request, 'account_system/registration.html', context)




def two_factor_auth_qr_code(request):
    user_name = cache.get(f'user_name')
    secret_key = cache.get(f"2fa_secret_key_{user_name}")
    if user_name and secret_key:
        qr_code = generate_qr_code(username=user_name, secret=secret_key)
        buffer = BytesIO()
        qr_code.save(buffer, format='PNG')

        buffer_value = buffer.getvalue()
        # Pass the QR code bytes as part of the context data
        qr_code = base64.b64encode(buffer_value).decode('utf-8')

        if request.method == 'GET':

            return render(
                request,
                'account_system/two_factor_auth_qrcode.html',
                {'qr_code': qr_code}
            )

        elif request.method == 'POST':
            verification_code = request.POST['verification_code']
            if verify_otp(secret=secret_key, otp=verification_code):
                username = cache.get('user_name')
                cache.delete(f"2fa_secret_key_{username}")
                cache.delete(f'user_name')
                cache.delete(f'phone_num')
                return redirect('login')
            else:
                errors = {'verification_code': 'Invalid verification code'}
                return render(
                    request,
                    'account_system/two_factor_auth_qrcode.html',
                    {'errors': errors, 'qr_code': qr_code}
                )

    return redirect('register')


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password1 = form.cleaned_data['password1']

            try:
                user = authenticate(
                    request,
                    phone_number=phone_number,
                    password=password1
                )
            except:
                try:
                    check_user = User.objects.get(phone_number=phone_number)
                except User.DoesNotExist:
                    errors = {'phone_number': 'User with such a phone number does not exist.'}
                    return render(request, 'account_system/login.html', {'errors': errors})
                errors = {'password1': 'Wrong password.'}
                return render(request, 'account_system/login.html', {'errors': errors})
            if not isinstance(user, dict):
                cache.set(f"2fa_secret_key_{user.name}", user.secret_code, 300)
                cache.set(f'phone_num', user.phone_number, 300)
                return redirect('two_factor_auth')

            else:
                return render(request, 'account_system/login.html', user)
        else:
            context = {
                'form': form,
                'errors': form.errors
            }
            return render(request, 'account_system/login.html', context)
    return render(request, 'account_system/login.html', {'form': LoginForm()})


def account_view(request, currency):
    if isinstance(request.user, User):
        phone_num = request.user.phone_number
        accounts = Account.objects.filter(owner__phone_number=phone_num, currency__name=currency)
        return render(request, 'account_system/account.html', {'accounts': accounts})
    return redirect('login')


def accounts_view(request):
    if isinstance(request.user, User):
        phone_num = request.user.phone_number
        accounts = Account.objects.filter(owner__phone_number=phone_num)
        return render(request, 'account_system/account.html', {'accounts': accounts})
    return redirect('login')


def two_factor_auth(request):
    phone_num = cache.get('phone_num')
    try:
        user = User.objects.get(phone_number=phone_num)
        secret_key = cache.get(f"2fa_secret_key_{user.name}")
    except User.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        verification_code = request.POST['verification_code']

        if verify_otp(secret=secret_key, otp=verification_code):
            login(request, user)
            cache.delete('phone_num')
            cache.delete(f"2fa_secret_key_{user.name}")
            loyalty_program(request)
            return redirect('home')

        else:
            errors = {
                'verification_code': 'Invalid verification code',
            }
            return render(
                request,
                'account_system/two_factor_auth.html',
                {'errors': errors}
            )

    else:
        return render(request, 'account_system/two_factor_auth.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def my_accounts_list(request):
    user = request.user
    if isinstance(user, User):
        accounts = Account.objects.filter(owner=user.pk)
        return render(request, 'account_system/my_accounts_list.html',
                        {'accounts': accounts})
    else:
        return redirect('home')

def create_account(request):
    user = request.user
    if isinstance(user, User):
        if request.method == 'POST':
            currency = Currency.objects.get(name=request.POST['currency'])
            amount = Decimal(random.uniform(1000.00, 10000.00))
            Account.objects.create(amount=amount, owner=user, currency=currency)
            return redirect('my_accounts_list')
        else:
            currencies = Currency.objects.all().values_list('name', flat=True)
            user_currencies = Account.objects.filter(owner=user.pk).values_list('currency__name', flat=True)
            available_currencies = [currency for currency in currencies if currency not in user_currencies]
            return render(request, 'account_system/create_account.html',
                          {'currencies': available_currencies})
    else:
        return redirect('home')