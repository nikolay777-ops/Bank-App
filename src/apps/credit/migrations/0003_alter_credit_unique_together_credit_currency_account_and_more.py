# Generated by Django 4.2.6 on 2023-12-10 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency_rates', '0003_alter_currencyaccount_balance'),
        ('credit', '0002_credit_closed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='credit',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='credit',
            name='currency_account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_currency_account', to='currency_rates.currencyaccount'),
        ),
        migrations.AlterField(
            model_name='creditpayment',
            name='payment_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Payment date'),
        ),
        migrations.RemoveField(
            model_name='credit',
            name='user',
        ),
    ]
