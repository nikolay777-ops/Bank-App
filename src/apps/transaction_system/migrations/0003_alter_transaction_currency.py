# Generated by Django 4.2.6 on 2023-12-10 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0009_alter_account_amount'),
        ('transaction_system', '0002_transaction_accepted_transaction_commission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_currency', to='account_system.currency'),
        ),
    ]