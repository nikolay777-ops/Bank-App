# Generated by Django 4.2.6 on 2023-12-07 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('currency_rates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remittance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.DecimalField(decimal_places=2, max_digits=6)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=5)),
                ('success', models.BooleanField(default=False)),
                ('currency', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='currency_rates.currency')),
                ('receiver', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='remittance_receiver', to='user.user')),
                ('sender', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='remittance_sender', to='user.user')),
            ],
            options={
                'verbose_name': 'Remittance',
                'verbose_name_plural': 'Remittances',
            },
        ),
    ]