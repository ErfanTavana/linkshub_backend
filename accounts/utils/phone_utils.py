from linkshub_backend.core.exceptions import CustomValidationError
from linkshub_backend.core.error_codes import ErrorCodes


def raise_phone_validation_error():
    raise CustomValidationError(
        success=False,
        message=ErrorCodes.INVALID_PHONE_NUMBER["message"],
        code=ErrorCodes.INVALID_PHONE_NUMBER["code"],
        status_code=ErrorCodes.INVALID_PHONE_NUMBER["status_code"],
        errors=ErrorCodes.INVALID_PHONE_NUMBER["errors"]
    )


def format_phone_number(phone_number: str):
    if not phone_number or not isinstance(phone_number, str):
        raise_phone_validation_error()

    phone_number_str = phone_number.strip()

    # تبدیل به فرمت استاندارد
    if phone_number_str.startswith('+98'):
        phone_number_str = '0' + phone_number_str[3:]
    elif phone_number_str.startswith('98'):
        phone_number_str = '0' + phone_number_str[2:]
    elif phone_number_str.startswith('0'):
        pass  # شماره تلفن در فرمت استاندارد است
    else:
        raise_phone_validation_error()

    if phone_number_str.startswith('09') and len(phone_number_str) == 11:
        return phone_number_str

    raise_phone_validation_error()
