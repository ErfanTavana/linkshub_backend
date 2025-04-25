from django.db import models
import random
import string
from datetime import timedelta

from django.conf import settings  # Import settings to use configured values
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

from accounts.constants import (
    OTP_API_KEY,
    OTP_VALIDITY_MINUTES,
    OTP_LENGTH,
    OTP_REQUEST_LIMIT_HOURS,
    OTP_REQUEST_LIMIT,
    OTP_LOCKED_TIME_MINUTES,
    OTP_FAILED_ATTEMPTS_LIMIT
)


from django.db import models
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.constants import (
    OTP_API_KEY,
    OTP_VALIDITY_MINUTES,
    OTP_LENGTH,
    OTP_REQUEST_LIMIT_HOURS,
    OTP_REQUEST_LIMIT,
    OTP_LOCKED_TIME_MINUTES,
    OTP_FAILED_ATTEMPTS_LIMIT
)

User = get_user_model()


class OTPCode(models.Model):
    """مدل ذخیره‌سازی کدهای تأیید برای عملیات‌هایی مثل ثبت‌نام و بازیابی رمز عبور."""

    CODE_TYPE_CHOICES = [
        ('registration', 'Registration'),
        ('password_reset', 'Password Reset'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    random_code = models.CharField(max_length=OTP_LENGTH, blank=True, null=True, verbose_name='کد تصادفی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    expires_at = models.DateTimeField(verbose_name='تاریخ انقضاء')
    failed_attempts = models.IntegerField(default=0, verbose_name='تعداد تلاش‌های ناموفق')
    is_valid = models.BooleanField(default=True, verbose_name='وضعیت اعتبار')
    ip = models.CharField(max_length=40, blank=True, null=True, verbose_name='آدرس IP')
    code_type = models.CharField(max_length=20, choices=CODE_TYPE_CHOICES, verbose_name='نوع کد')
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name="قفل شده تا")
