"""
URL configuration for bank_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from credit_system.views import credit_configuration_list, user_credit_list
from account_system.views import (
    register,
    home,
    two_factor_auth_qr_code,
    login_view,
    two_factor_auth,
    logout_view,
    accounts_view,
    account_view,
    create_account,
    my_accounts_list,
)
from transaction_system.views import transaction_history, create_transaction, view_incoming_transactions
from stats_system.views import statistics_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', register, name='register'),
    path('two_factor_auth_qrcode/', two_factor_auth_qr_code, name='two_factor_auth_qrcode'),
    path('', home, name='home'),
    path('login/', login_view, name="login"),
    path('two_factor_auth/', two_factor_auth, name="two_factor_auth"),
    path('logout/', logout_view, name="logout"),
    path('accounts/<str:currency>', account_view, name='account_list'),
    path('accounts/', accounts_view, name='accounts_list'),

    path('create_account', create_account, name='create_account'),
    path('my_accounts_list/', my_accounts_list, name='my_accounts_list'),

    path('create_transaction/', create_transaction, name="create_transaction"),
    path('view_incoming_transactions/', view_incoming_transactions, name="view_incoming_transactions"),
    path('transaction_history/', transaction_history, name="transaction_history"),

    path('credits/', credit_configuration_list, name='credits_list'),
    path('my_credits/', user_credit_list, name="user_credit_list"),
    path('take_credit/', login_view, name="take_credit"),

    path('my_stats/', statistics_view, name="my_stats"),

]
