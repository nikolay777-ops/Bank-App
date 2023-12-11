# Generated by Django 4.2.6 on 2023-12-10 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('closed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Credit',
                'verbose_name_plural': 'Credits',
            },
        ),
        migrations.CreateModel(
            name='CreditPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='The amount for payment')),
                ('payment_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Payment date')),
                ('credit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_payment_credit', to='credit_system.credit')),
            ],
            options={
                'verbose_name': 'CreditPayment',
                'verbose_name_plural': 'CreditPayments',
            },
        ),
        migrations.CreateModel(
            name='CreditConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('term_months', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=15)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account_system.currency')),
            ],
            options={
                'verbose_name': 'Credit Configuration',
                'verbose_name_plural': 'Credit Configurations',
            },
        ),
        migrations.AddField(
            model_name='credit',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_configuration', to='credit_system.creditconfiguration'),
        ),
        migrations.AddField(
            model_name='credit',
            name='currency_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_currency_account', to='account_system.account'),
        ),
    ]