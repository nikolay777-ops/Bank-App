# Generated by Django 4.2.6 on 2023-12-10 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0008_alter_user_role_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount of money'),
        ),
    ]