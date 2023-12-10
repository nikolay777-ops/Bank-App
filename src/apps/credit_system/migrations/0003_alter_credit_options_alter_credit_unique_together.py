# Generated by Django 4.2.6 on 2023-12-09 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0006_remove_user_account_id'),
        ('credit_system', '0002_credit_creditconfiguration_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credit',
            options={'verbose_name': 'Credit', 'verbose_name_plural': 'Credits'},
        ),
        migrations.AlterUniqueTogether(
            name='credit',
            unique_together={('user', 'configuration')},
        ),
    ]