import base64
from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Account, Role
from .infrastructure.services.two_factor_auth import generate_secret_key, generate_qr_code, verify_otp
from django.core.cache import cache


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохранение формы, но не коммитить в базу данных
            user.role_id = Role.objects.get(id=1)
            user.account_id = Account.objects.create(amount=0.00)  # Установка объекта Account в поле account_id
            secret_key = generate_secret_key()
            user.secret_code = secret_key
            user.save()

            # cache user-secret code
            cache.set(f'user_name', user.name, 300)
            cache.set(f"2fa_secret_key_{user.name}", secret_key, 300)

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
    if request.method == 'GET':

        user_name = cache.get(f'user_name')
        if user_name:
            # cache.delete(f'user_name')
            secret_key = cache.get(f"2fa_secret_key_{user_name}")
            if secret_key:
                # Delete the secret key from cache after retrieving it
                # cache.delete(f"2fa_secret_key_{request.user.id}")

                qr_code = generate_qr_code(username=user_name, secret=secret_key)
                buffer = BytesIO()
                qr_code.save(buffer, format='PNG')

                buffer_value = buffer.getvalue()
                # Pass the QR code bytes as part of the context data
                qr_code = base64.b64encode(buffer_value).decode('utf-8')

                return render(
                    request,
                    'account_system/two_factor_auth_qrcode.html',
                    {'qr_code': qr_code}
                )

        return redirect('login')

    elif request.method == 'POST':
        user_name = cache.get(f'user_name')
        if user_name:
            # cache.delete(f'user_name')
            secret_key = cache.get(f"2fa_secret_key_{user_name}")
            if secret_key:
                verification_code = request.POST['verification_code']
                if verify_otp(secret=secret_key, otp=verification_code):
                    return redirect('home')
                else:
                    return render(
                        request,
                        'account_system/two_factor_auth_qrcode.html',
                        {'error': 'Invalid verification code'}
                    )

        return render(
            request,
            'account_system/two_factor_auth_qrcode.html',
            {'qr_code': None}
        )

def home(request):
    # You can add any additional logic or data retrieval here if needed
    return render(request, 'core/home.html')