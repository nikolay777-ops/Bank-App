from django.contrib import admin
from django.urls import path
from user.views import register, home, two_factor_auth_qr_code, login_view, two_factor_auth, accounts_view, account_view
from credit.views import credit_configuration_list

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', register, name='register'),
    path('two_factor_auth_qrcode/', two_factor_auth_qr_code, name='two_factor_auth_qrcode'),
    path('', home, name='home'),
    path('login/', login_view, name="login"),
    path('two_factor_auth/', two_factor_auth, name="two_factor_auth"),

    path('create_transaction/', login_view, name="create_transaction"),

    path('credits/', credit_configuration_list, name='credits_list'),
    path('my_credits/', two_factor_auth, name="my_credits"),
    path('take_credit/', login_view, name="take_credit"),

    path('my_stats/', two_factor_auth, name="my_stats"),
    path('accounts/<str:currency>', account_view, name='account_list'),
    path('accounts/', accounts_view, name='accounts_list'),
]