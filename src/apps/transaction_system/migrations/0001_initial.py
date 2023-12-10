# Generated by Django 4.2.6 on 2023-12-07 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount of $')),
                ('timestamp', models.DateTimeField(verbose_name='The date of the transaction')),
                ('corespondent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_corespondents', to='account_system.user')),
                ('recipient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_recipients', to='account_system.user')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]