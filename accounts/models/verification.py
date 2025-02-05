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

from linkshub_backend.settings import VERIFICATION_CODE_API_KEY, VERIFICATION_CODE_VALIDITY_MINUTES, \
    VERIFICATION_CODE_LENGTH, VERIFICATION_CODE_REQUEST_LIMIT_HOURS, VERIFICATION_CODE_REQUEST_LIMIT, \
    VERIFICATION_CODE_REQUEST_LIMIT, LOCKED_TIME_MINUTES, FAILED_ATTEMPTS_LIMIT


class VerificationCode(models.Model):
    """
    Model to store verification codes for user actions like registration and password reset.
    """
    CODE_TYPE_CHOICES = [
        ('registration', 'Registration'),
        ('password_reset', 'Password Reset'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر'
    )
    random_code = models.CharField(
        max_length=VERIFICATION_CODE_LENGTH, blank=True, null=True, verbose_name='کد تصادفی'
    )  # The verification code
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد'
    )  # Timestamp when the code was created
    expires_at = models.DateTimeField(
        verbose_name='تاریخ انقضاء'
    )  # Timestamp when the code expires
    failed_attempts = models.IntegerField(
        default=0, verbose_name='تعداد تلاش‌های ناموفق'
    )  # Counter for failed verification attempts
    is_valid = models.BooleanField(
        default=True, verbose_name='وضعیت اعتبار'
    )  # Indicates if the code is still valid
    ip = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='آدرس IP'
    )  # IP address from which the code was requested
    code_type = models.CharField(
        max_length=20, choices=CODE_TYPE_CHOICES, verbose_name='نوع کد'
    )  # Type of the verification code
    locked_until = models.DateTimeField(null=True, blank=True,
                                        verbose_name="قفل شده تا")  # Timestamp until which the code is locked

    @staticmethod
    def generate_random_code():
        """
        Generate a random numeric verification code of specified length from settings.
        """
        return ''.join(random.choices('0123456789', k=VERIFICATION_CODE_LENGTH))

    @classmethod
    def create_verification_code(cls, user, code_type):
        """
        Create a new verification code for a user if conditions allow.
        """
        latest_verification = cls.objects.filter(user=user, code_type=code_type).order_by('-created_at').first()
        if latest_verification:
            if latest_verification.is_locked():
                remaining_time = (latest_verification.locked_until - timezone.now()).total_seconds() // 60
                return None, f"شما به دلیل تلاش بیش از حد تا {int(remaining_time)} دقیقه‌ی دیگر محدود هستید."

            if latest_verification.has_valid_code():
                remaining_seconds = (latest_verification.expires_at - timezone.now()).total_seconds()
                remaining_minutes = int(remaining_seconds // 60)
                remaining_seconds = int(remaining_seconds % 60)

                if remaining_minutes > 0:
                    return None, f"کد تأیید قبلی هنوز منقضی نشده است. لطفاً {remaining_minutes} دقیقه و {remaining_seconds} ثانیه دیگر مجدداً امتحان کنید."
                else:
                    return None, f"کد تأیید قبلی هنوز منقضی نشده است. لطفاً {remaining_seconds} ثانیه دیگر مجدداً امتحان کنید."

            if latest_verification.has_exceeded_request_limit():
                limit_hours = VERIFICATION_CODE_REQUEST_LIMIT_HOURS
                request_limit = VERIFICATION_CODE_REQUEST_LIMIT
                time_threshold = timezone.now() - timedelta(hours=limit_hours)
                request_count = VerificationCode.objects.filter(
                    user=user, created_at__gte=time_threshold, code_type=code_type
                ).count()

                # محاسبه زمان بعدی که کاربر می‌تواند درخواست جدید ارسال کند
                next_request_time = VerificationCode.objects.filter(
                    user=user, created_at__gte=time_threshold, code_type=code_type
                ).order_by('-created_at').first().created_at + timedelta(hours=limit_hours)

                remaining_time = next_request_time - timezone.now()
                remaining_hours = int(remaining_time.total_seconds() // 3600)
                remaining_minutes = int((remaining_time.total_seconds() % 3600) // 60)

                return None, f"شما {request_count} درخواست از حداکثر {request_limit} درخواست مجاز خود در {limit_hours} ساعت گذشته را انجام داده‌اید. لطفاً {remaining_hours} ساعت و {remaining_minutes} دقیقه دیگر مجدداً امتحان کنید."

        verification_code = cls(
            user=user,
            random_code=cls.generate_random_code(),
            expires_at=timezone.now() + timedelta(minutes=VERIFICATION_CODE_VALIDITY_MINUTES),
            code_type=code_type
        )
        verification_code.save()
        return verification_code, None

    def is_locked(self):
        """
        Check if the verification code is currently locked.
        """
        return self.locked_until and timezone.now() < self.locked_until

    def lock_for(self, minutes):
        """
        Lock the verification code for a specified number of minutes.
        """
        self.locked_until = timezone.now() + timedelta(minutes=minutes)
        self.save()

    def has_valid_code(self):
        """
        Determine if the verification code is still valid.
        """
        return self.is_valid and timezone.now() < self.expires_at

    def has_exceeded_request_limit(self):
        """
        Check if the user has exceeded the limit for requesting verification codes within a time frame.
        """
        limit_hours = VERIFICATION_CODE_REQUEST_LIMIT_HOURS
        request_limit = VERIFICATION_CODE_REQUEST_LIMIT
        time_threshold = timezone.now() - timedelta(hours=limit_hours)
        request_count = VerificationCode.objects.filter(
            user=self.user, created_at__gte=time_threshold, code_type=self.code_type
        ).count()
        return request_count >= request_limit

    class Meta:
        verbose_name = "کد تایید"  # Singular name in admin
        verbose_name_plural = 'کد های تایید'  # Plural name in admin
