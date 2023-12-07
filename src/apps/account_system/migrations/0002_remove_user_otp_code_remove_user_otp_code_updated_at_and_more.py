# Generated by Django 4.2.6 on 2023-12-07 21:20

from django.db import migrations, models
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='otp_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_code_updated_at',
        ),
        migrations.AddField(
            model_name='user',
            name='secret_code',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True, verbose_name='secret code'),
        ),
        migrations.AddField(
            model_name='user',
            name='secret_code_updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Date and time of secret code update'),
        ),
    ]
