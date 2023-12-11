import base64
from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect

import constants.currency
from currency_rates.models import CurrencyAccount
from .forms import RegistrationForm, LoginForm
from .models import User
from .infrastructure.services.oauth import generate_secret_key, generate_qr_code, verify_otp
from django.core.cache import cache

from django.contrib.auth import login, authenticate, logout


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохранение формы, но не коммитить в базу данных
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
    else:
        form = RegistrationForm()
        context = {
            'form': form
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
                user = User.objects.get(phone_number=cache.get('phone_num'))
                CurrencyAccount.objects.create(
                    currency_id=constants.currency.CURRENCY_CODE_USD,
                    user=user,
                    balance=5000
                ).save()
                CurrencyAccount.objects.create(
                    currency_id=constants.currency.CURRENCY_CODE_BYN,
                    user=user,
                    balance=5000
                ).save()
                CurrencyAccount.objects.create(
                    currency_id=constants.currency.CURRENCY_CODE_RUB,
                    user=user,
                    balance=5000
                ).save()
                cache.delete(f'phone_num')

                return redirect('login')
            else:
                errors = {'verification_code': ['Invalid verification code']}
                return render(
                    request,
                    'account_system/two_factor_auth_qrcode.html',
                    {'errors': errors, 'qr_code': qr_code}
                )

    return redirect('register')


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if isinstance(request.user, AnonymousUser):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data['phone_number']
                password1 = form.cleaned_data['password1']

                user = authenticate(
                    request,
                    phone_number=phone_number,
                    password=password1
                )
                if user is not None:
                    cache.set(f"2fa_secret_key_{user.name}", user.secret_code, 300)
                    cache.set(f'phone_num', user.phone_number, 300)
                    return redirect('two_factor_auth')
                else:
                    errors = {'error': 'Invalid phone number of password'}
                    context = {
                        'form': form,
                        'errors': errors
                    }
                    return render(request, 'account_system/login.html', context)

        return render(request, 'account_system/login.html', {'form': LoginForm()})

    return redirect('home')

def account_view(request, currency):
    if isinstance(request.user, User):
        phone_num = request.user.phone_number
        accounts = CurrencyAccount.objects.filter(user__phone_number=phone_num, currency__name=currency)
        return render(request, 'account_system/account.html', {'accounts': accounts})
    return redirect('login')


def accounts_view(request):
    if isinstance(request.user, User):
        phone_num = request.user.phone_number
        accounts = CurrencyAccount.objects.filter(user__phone_number=phone_num)
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
            return redirect('home')

        else:
            errors = {
                'verification_code': [
                    'Invalid verification code',
                ]
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
