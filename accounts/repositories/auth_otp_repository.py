from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.utils import format_phone_number
from linkshub_backend.core.exceptions import CustomValidationError
from accounts.models import OTPCode
from django.utils import timezone
from datetime import timedelta
import random

from accounts.constants import OTP_REQUEST_LIMIT_HOURS, OTP_REQUEST_LIMIT, OTP_VALIDITY_MINUTES, OTP_LENGTH

User = get_user_model()


def get_or_create_user_by_phone(phone_number: str):
    with transaction.atomic():
        user, created = User.objects.get_or_create(phone_number=phone_number, defaults={"is_active": True})
        return user, created


def get_latest_otp(user, code_type):
    """دریافت آخرین کد OTP کاربر"""
    latest_otp = OTPCode.objects.filter(user=user, code_type=code_type).order_by('-created_at').first()
    return latest_otp


def has_exceeded_request_limit(user, code_type):
    """
    بررسی می‌کند که آیا کاربر حد مجاز درخواست کد تأیید را در یک بازه زمانی خاص نقض کرده است یا نه.
    """
    limit_hours = OTP_REQUEST_LIMIT_HOURS
    request_limit = OTP_REQUEST_LIMIT
    time_threshold = timezone.now() - timedelta(hours=limit_hours)

    request_count = OTPCode.objects.filter(
        user=user, created_at__gte=time_threshold, code_type=code_type
    ).count()

    return request_count >= request_limit


def get_next_request_time(user, code_type):
    """
    زمان بعدی که کاربر می‌تواند درخواست کد تأیید ارسال کند را محاسبه می‌کند.
    """
    limit_hours = OTP_REQUEST_LIMIT_HOURS
    time_threshold = timezone.now() - timedelta(hours=limit_hours)

    # گرفتن آخرین درخواست
    latest_verification = OTPCode.objects.filter(
        user=user, created_at__gte=time_threshold, code_type=code_type
    ).order_by('-created_at').first()

    if latest_verification:
        return latest_verification.created_at + timedelta(hours=limit_hours)
    return timezone.now()


def generate_otp_code():
    """تولید یک کد تصادفی OTP"""
    return ''.join(random.choices('0123456789', k=OTP_LENGTH))


def create_otp(user, code_type, ip_address):
    """
    Creates and saves a new OTP code for the user with the specified code type and IP address.
    The code will expire in the configured time limit.
    """
    expiration_time = timezone.now() + timedelta(minutes=OTP_VALIDITY_MINUTES)

    verification_code = generate_otp_code()

    otp = OTPCode.objects.create(
        user=user,
        random_code=verification_code,
        expires_at=expiration_time,
        ip=ip_address,
        code_type=code_type,
        is_valid=True
    )
    return otp
