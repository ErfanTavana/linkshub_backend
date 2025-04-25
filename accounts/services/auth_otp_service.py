from accounts.utils import format_phone_number
from linkshub_backend.core.exceptions import CustomValidationError
from accounts.repositories import get_or_create_user_by_phone, get_latest_otp, has_exceeded_request_limit, \
    get_next_request_time
from django.utils import timezone
from linkshub_backend.core.error_codes import ErrorCodes, SuccessCodes
from accounts.constants import OTP_SMS_TEMPLATE, OTP_API_KEY
import ghasedakpack
from accounts.utils import format_phone_number
from linkshub_backend.core.exceptions import CustomValidationError
from accounts.repositories import get_or_create_user_by_phone,create_otp, get_latest_otp
from linkshub_backend.core.error_codes import SuccessCodes
from accounts.constants import OTP_VALIDITY_MINUTES, OTP_LENGTH

def check_locked_verification(latest_otp):
    """
    بررسی می‌کند که آیا آخرین کد تأیید کاربر قفل شده است یا نه.
    اگر قفل باشد، پیام و زمان باقی‌مانده را برمی‌گرداند.
    """
    if latest_otp and latest_otp.locked_until and timezone.now() < latest_otp.locked_until:
        # remaining_time = (latest_otp.locked_until - timezone.now()).total_seconds() // 60
        raise CustomValidationError(
            success=False,
            message=ErrorCodes.ACCOUNT_LOCKED["message"],
            code=ErrorCodes.ACCOUNT_LOCKED["code"],
            status_code=ErrorCodes.ACCOUNT_LOCKED["status_code"],
            errors=ErrorCodes.ACCOUNT_LOCKED["errors"]
        )
    return {
        "success": True,
        "code": SuccessCodes.ACCOUNT_NOT_LOCKED["code"],
        "message": SuccessCodes.ACCOUNT_NOT_LOCKED["message"],
        "data": {}
    }


def check_active_otp(latest_otp):
    if latest_otp and latest_otp.is_valid and timezone.now() < latest_otp.expires_at:
        remaining_seconds = (latest_otp.expires_at - timezone.now()).total_seconds()
        remaining_minutes = int(remaining_seconds // 60)
        remaining_seconds = int(remaining_seconds % 60)
        data = {
            "remaining_minutes": remaining_minutes,
            "remaining_seconds": remaining_seconds
        }
        raise CustomValidationError(
            success=False,
            message=ErrorCodes.OTP_NOT_EXPIRED['message'],
            code=ErrorCodes.OTP_NOT_EXPIRED["code"],
            status_code=ErrorCodes.OTP_NOT_EXPIRED["status_code"],
            errors=ErrorCodes.OTP_NOT_EXPIRED["errors"],
            data=data
        )


def check_request_limit(user, code_type):
    """
    بررسی می‌کند که آیا کاربر حد مجاز درخواست‌های کد تأیید را نقض کرده است یا نه و زمان باقیمانده برای درخواست بعدی را محاسبه می‌کند.
    """
    if has_exceeded_request_limit(user, code_type):
        next_request_time = get_next_request_time(user, code_type)
        remaining_time = next_request_time - timezone.now()
        remaining_hours = int(remaining_time.total_seconds() // 3600)
        remaining_minutes = int((remaining_time.total_seconds() % 3600) // 60)

        raise CustomValidationError(
            success=False,
            message=ErrorCodes.VERIFICATION_REQUEST_LIMIT_EXCEEDED["message"],
            code=ErrorCodes.VERIFICATION_REQUEST_LIMIT_EXCEEDED["code"],
            status_code=ErrorCodes.VERIFICATION_REQUEST_LIMIT_EXCEEDED["status_code"],
            errors=ErrorCodes.VERIFICATION_REQUEST_LIMIT_EXCEEDED["errors"],
            data={
                "remaining_hours": remaining_hours,
                "remaining_minutes": remaining_minutes
            }
        )
    return True


def send_otp_verification_sms(phone_number, verification_code):
    """
    ارسال کد تأیید OTP به شماره تلفن از طریق سرویس پیامکی قاصدک.
    """
    sms = ghasedakpack.Ghasedak(OTP_API_KEY)
    verification_code_str = str(verification_code)
    template = OTP_SMS_TEMPLATE

    response = sms.verification({
        'receptor': phone_number,
        'type': '1',
        'template': template,
        'param1': phone_number,
        'param2': verification_code_str
    })
    if not response:
        raise CustomValidationError(
            success=False,
            message=ErrorCodes.VERIFICATION_CODE_SENDING_FAILED["message"],
            code=ErrorCodes.VERIFICATION_CODE_SENDING_FAILED["code"],
            status_code=ErrorCodes.VERIFICATION_CODE_SENDING_FAILED["status_code"],
            errors=ErrorCodes.VERIFICATION_CODE_SENDING_FAILED["errors"],
            data={}
        )
    return response
def send_otp(phone_number: str, ip_address: str, code_type: str = "registration"):
    try:
        # فرمت شماره
        phone_number = format_phone_number(phone_number)

        # گرفتن یا ساخت کاربر
        user, created = get_or_create_user_by_phone(phone_number=phone_number)

        # بررسی محدودیت درخواست‌های قبلی
        check_request_limit(user, code_type)

        # گرفتن آخرین OTP کاربر
        latest_otp = get_latest_otp(user, code_type)

        # بررسی قفل بودن OTP
        check_locked_verification(latest_otp)

        # بررسی معتبر بودن OTP قبلی
        check_active_otp(latest_otp)

        # تولید OTP جدید
        otp = create_otp(user=user, code_type=code_type, ip_address=ip_address)

        # ارسال پیامک OTP
        send_otp_verification_sms(phone_number, otp.random_code)

        # پاسخ موفق
        return {
            "success": True,
            "message": SuccessCodes.OTP_SENT_SUCCESSFULLY["message"],
            "code": SuccessCodes.OTP_SENT_SUCCESSFULLY["code"],
            "data": {
                "expires_in_minutes": OTP_VALIDITY_MINUTES,  # مدت زمان انقضا
                "otp_length": OTP_LENGTH,  # طول کد تایید
                "phone_number": phone_number,  # شماره موبایل
                "ip_address": ip_address,  # آی‌پی درخواست
            }
        }


    except CustomValidationError as e:
        # مدیریت خطاهای سفارشی
        return {
            "success": e.success,
            "message": e.message,
            "errors": e.errors or [],
            "code": e.code,
            "data": e.data or {}
        }
