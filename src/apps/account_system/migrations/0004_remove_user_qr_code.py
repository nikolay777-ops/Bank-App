# Generated by Django 4.2.6 on 2023-12-08 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='qr_code',
        ),
    ]