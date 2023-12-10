# Generated by Django 4.2.6 on 2023-12-09 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_user', to='user.user')),
            ],
            options={
                'verbose_name': 'Investment portfolio',
                'verbose_name_plural': 'Investment portfolios',
            },
        ),
        migrations.CreateModel(
            name='InvestmentStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe_commission', models.FloatField()),
                ('revenue_commission', models.FloatField()),
                ('investment_portfolio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stocks.investmentportfolio')),
            ],
            options={
                'verbose_name': 'Investment Strategy',
                'verbose_name_plural': 'Investment Strategies',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('name', models.CharField(choices=[('AAPL', 'AAPL'), ('TSLA', 'TSLA'), ('AMZN', 'AMZN'), ('META', 'META'), ('GOOG', 'GOOG')], primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
            },
        ),
        migrations.CreateModel(
            name='StockPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('date_of_use', models.DateTimeField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),
            ],
            options={
                'verbose_name': 'Stock price',
                'verbose_name_plural': 'Stock prices',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.investmentstrategy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber_user', to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='StockTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy', models.BooleanField(default=True)),
                ('count', models.IntegerField()),
                ('inv_portfolio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_inv_port', to='stocks.investmentportfolio')),
                ('stock_price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stockprices')),
            ],
            options={
                'verbose_name': 'Stock transaction',
                'verbose_name_plural': 'Stock transactions',
            },
        ),
    ]