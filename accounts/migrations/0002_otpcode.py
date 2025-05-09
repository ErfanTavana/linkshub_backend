# Generated by Django 5.1.5 on 2025-02-17 09:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('random_code', models.CharField(blank=True, max_length=4, null=True, verbose_name='کد تصادفی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('expires_at', models.DateTimeField(verbose_name='تاریخ انقضاء')),
                ('failed_attempts', models.IntegerField(default=0, verbose_name='تعداد تلاش\u200cهای ناموفق')),
                ('is_valid', models.BooleanField(default=True, verbose_name='وضعیت اعتبار')),
                ('ip', models.CharField(blank=True, max_length=40, null=True, verbose_name='آدرس IP')),
                ('code_type', models.CharField(choices=[('registration', 'Registration'), ('password_reset', 'Password Reset')], max_length=20, verbose_name='نوع کد')),
                ('locked_until', models.DateTimeField(blank=True, null=True, verbose_name='قفل شده تا')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کد تایید',
                'verbose_name_plural': 'کد های تایید',
            },
        ),
    ]
