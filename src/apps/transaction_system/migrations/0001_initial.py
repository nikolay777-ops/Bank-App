# Generated by Django 4.2.6 on 2023-12-10 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_system', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoyaltyConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='min amount of money')),
                ('percent', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='%')),
            ],
            options={
                'verbose_name': 'LoyaltyConfig',
                'verbose_name_plural': 'LoyaltyConfigs',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount of money')),
                ('timestamp', models.DateTimeField(verbose_name='The date of the transaction')),
                ('commission', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Commission')),
                ('success', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('corespondent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_corespondents', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_currency', to='account_system.currency')),
                ('recipient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_recipients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]