import base64
from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm
from .models import Account, Role, User
from .infrastructure.services.two_factor_auth import generate_secret_key, generate_qr_code, verify_otp
from django.core.cache import cache

from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохранение формы, но не коммитить в базу данных
            user.role_id = Role.objects.get(id=1)
            secret_key = generate_secret_key()
            user.secret_code = secret_key
            user.save()

            # cache user-secret code
            cache.set(f'user_name', user.name, 3600)
            cache.set(f"2fa_secret_key_{user.name}", secret_key, 3600)
            cache.set(f'phone_num', user.phone_number, 3600)

            return redirect('two_factor_auth_qrcode')

        else:
            context = {
                'form': form,
                'errors': form.errors
            }
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
                return redirect('home')
            else:
                errors = {'verification_code': ['Invalid verification code']}
                return render(
                    request,
                    'account_system/two_factor_auth_qrcode.html',
                    {'errors': errors, 'qr_code': qr_code}
                )

    return redirect('register')


def home(request):
    # You can add any additional logic or data retrieval here if needed
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = False
    if user_id and user:
        return render(request, 'core/home.html', {'user': user})
    else:
        return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password1 = form.cleaned_data['password1']

            # Проверяем пользователя по номеру телефона
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.check_password(password1):
                    login(request, user)
                    request.session['user_id'] = user.id
                    secret_key = user.secret_code

                    # cache user-secret code
                    cache.set(f'user_name', user.name, 3600)
                    cache.set(f"2fa_secret_key_{user.name}", secret_key, 3600)
                    cache.set(f'phone_num', user.phone_number, 3600)

                    return redirect('two_factor_auth')
                else:
                    errors = {'password1': ['Incorrect password']}
                    return render(request, 'account_system/login.html', {'form': form, 'errors': errors})
            except User.DoesNotExist:
                errors = {'phone_number': ['User with this phone number does not exist']}
                return render(request, 'account_system/login.html', {'form': form, 'errors': errors})
        else:
            errors = form.errors
            return render(request, 'account_system/login.html', {'form': form, 'errors': errors})
    else:
        form = LoginForm()
    return render(request, 'account_system/login.html', {'form': form})


def account_view(request, currency):
    user_name = cache.get(f'user_name')
    secret_key = cache.get(f"2fa_secret_key_{user_name}")
    phone_num = cache.get('phone_num')
    if user_name and secret_key:
        account = Account.objects.get(owner__name=user_name, owner__phone_number=phone_num, currency__name=currency)
        return render(request, 'account_system/account.html', {'accounts': [account]})

    return redirect('login')


def accounts_view(request):
    user_name = cache.get(f'user_name')
    secret_key = cache.get(f"2fa_secret_key_{user_name}")
    phone_num = cache.get('phone_num')
    if user_name and secret_key:
        accounts = Account.objects.filter(owner__name=user_name, owner__phone_number=phone_num)
        return render(request, 'account_system/account.html', {'accounts': accounts})

    return redirect('login')


def two_factor_auth(request):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = False
    if user_id and user:
        request.session['user_id'] = user_id
        if request.method == 'POST':
            user_name = cache.get(f'user_name')
            secret_key = cache.get(f"2fa_secret_key_{user_name}")
            if user_name and secret_key:
                verification_code = request.POST['verification_code']
                if verify_otp(secret=secret_key, otp=verification_code):
                    request.session['user_id'] = user_id
                    return redirect('home')
                else:
                    errors = {'verification_code': ['Invalid verification code']}
                    return render(
                        request,
                        'account_system/two_factor_auth.html',
                        {'errors': errors}
                    )
            else:
                return redirect('login')
        else:
            return render(request, 'account_system/two_factor_auth.html')
    else:
        return redirect('login')
