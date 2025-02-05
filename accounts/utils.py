from linkshub_backend.settings import VERIFICATION_CODE_API_KEY, SMS_TEMPLATE, LOCKED_TIME_MINUTES, \
    FAILED_ATTEMPTS_LIMIT
import ghasedakpack
from models import VerificationCode

from rest_framework import status

from rest_framework.response import Response


def format_phone_number(phone_number):
    if not phone_number or not isinstance(phone_number, str):
        raise ValueError("شماره تلفن نامعتبر است.")

    phone_number_str = phone_number.strip()

    if phone_number_str.startswith('+98'):
        phone_number_str = '0' + phone_number_str[3:]
    elif phone_number_str.startswith('98'):
        phone_number_str = '0' + phone_number_str[2:]
    elif phone_number_str.startswith('0'):
        pass  # شماره تلفن در فرمت استاندارد است
    else:
        raise ValueError("شماره تلفن نامعتبر است.")

    return phone_number_str



def send_registration_verification_code_sms(phone_number, verification_code):
    # Send an SMS containing the registration verification code using the Ghasedak service
    sms = ghasedakpack.Ghasedak(f"{VERIFICATION_CODE_API_KEY}")
    phone_number_str = format_phone_number(phone_number)
    verification_code_str = str(verification_code)
    template = SMS_TEMPLATE
    response = sms.verification({
        'receptor': f'{phone_number}',
        'type': '1',
        'template': template,
        'param1': f'{phone_number_str}',
        'param2': f'{verification_code_str}'
    })

    return response


def get_latest_verification_code(user):
    # Get the latest verification code for a given user
    return VerificationCode.objects.filter(user=user).order_by('-created_at').first()


def check_verification_code(verification_code, verification_code_input, expected_code_type):
    # Validate the provided verification code against the stored code
    if not verification_code:
        return Response(
            {"message": "کد تأیید معتبری برای این کاربر وجود ندارد.", "data": None},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the user is locked
    if verification_code.is_locked():
        return Response(
            {"message": "شما به دلیل تلاش‌های ناموفق مکرر نمی‌توانید تا ۳۰ دقیقه دیگر کد تأیید جدیدی دریافت کنید.",
             "data": None},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the code type matches the expected type
    if verification_code.code_type != expected_code_type:
        return Response(
            {"message": "نوع کد تأیید نادرست است.", "data": None},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the code is still valid
    if not verification_code.has_valid_code():
        verification_code.is_valid = False
        verification_code.save()
        return Response(
            {"message": "کد تأیید منقضی شده است.", "data": None},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the number of failed attempts has reached the limit
    if verification_code.failed_attempts >= FAILED_ATTEMPTS_LIMIT:
        verification_code.is_valid = False
        verification_code.lock_for(LOCKED_TIME_MINUTES)  # Lock the user for a specified period
        verification_code.save()
        return Response(
            {"message": "شما بیش از حد مجاز تلاش کرده‌اید. کد تأیید غیر فعال شد و شما به مدت ۳۰ دقیقه قفل شدید.",
             "data": None},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the provided code matches the stored code
    if verification_code_input != verification_code.random_code:
        verification_code.failed_attempts += 1
        if verification_code.failed_attempts >= FAILED_ATTEMPTS_LIMIT:
            verification_code.lock_for(LOCKED_TIME_MINUTES)  # Lock the user for a specified period
        verification_code.save()
        return Response(
            {"message": "کد تأیید اشتباه است.", "data": None},
            status=status.HTTP_400_BAD_REQUEST
        )

    return None
