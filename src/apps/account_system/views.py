import base64
from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from pyexpat.errors import messages

from .forms import RegistrationForm
from .models import Account, Role
from django.contrib.auth import login
from .infrastructure.services.two_factor_auth import generate_secret_key, generate_qr_code

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = Account.objects.create(amount=0.00)
            role = Role.objects.get(id=1)
            user = form.save(commit=False)  # Сохранение формы, но не коммитить в базу данных
            user.account_id = account  # Установка объекта Account в поле account_id
            user.role_id = role
            secret_key = generate_secret_key()
            user.secret_code = secret_key
            qr_code = generate_qr_code(user.name, secret_key)
            qr_code_image = qr_code
            buffer = BytesIO()
            qr_code.save(buffer, format='PNG')
            qr_code_filename = f'{user.name}_qr_code.png'
            user.qr_code.save(qr_code_filename, ContentFile(buffer.getvalue()), save=True)
            user.save()  # Сохранение объекта User

            # Создание сессии для зарегистрированного пользователя
            login(request, user)

            qr_bytes = BytesIO()
            qr_code_image.save(qr_bytes, format='PNG')

            # Pass the QR code bytes as part of the context data
            qr_base64 = base64.b64encode(qr_bytes.getvalue()).decode('utf-8')

            # Pass the base64 encoded QR code image as part of the context data
            context = {
                'qr_base64': qr_base64,
            }
            return render(request, 'account_system/two_factor_auth_qrcode.html', context)
        else:
            # Вывод ошибок в случае неудачной валидации
            errors = form.errors
            return render(request, 'account_system/registration.html', {'form': form, 'errors': errors})
    else:
        form = RegistrationForm()
    return render(request, 'account_system/registration.html', {'form': form})

def home(request):
    # You can add any additional logic or data retrieval here if needed
    return render(request, 'core/home.html')