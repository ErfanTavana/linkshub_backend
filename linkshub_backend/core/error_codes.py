from rest_framework import status


class SuccessCodes:
    ACCOUNT_NOT_LOCKED = {
        "code": "2001",
        "message": "حساب کاربری قفل نمیباشد.",
        'data': {},
    }
    OTP_SENT_SUCCESSFULLY = {
        "code": "2002",
        "message": "کد تایید با موفقیت ارسال شد.",
        "data": {},
    }


class ErrorCodes:
    # Common Errors
    ERROR = {
        "code": "4000",
        "message": "خطای عمومی رخ داده است.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    INVALID_PHONE_NUMBER = {
        "code": "4001",
        "message": "شماره تلفن نامعتبر است.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    INVALID_OTP = {
        "code": "4002",
        "message": "کد تأیید معتبر نمی‌باشد.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    OTP_EXPIRED = {
        "code": "4003",
        "message": "کد تأیید منقضی شده است.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    OTP_ATTEMPT_LIMIT_EXCEEDED = {
        "code": "4004",
        "message": "تعداد تلاش‌های شما برای وارد کردن کد تایید بیش از حد مجاز است.",
        'status_code': status.HTTP_429_TOO_MANY_REQUESTS,
        'errors': [],
        'data': {}
    }

    OTP_REQUEST_LIMIT_EXCEEDED = {
        "code": "4005",
        "message": "شما بیش از حد مجاز درخواست کد تأیید ارسال کرده‌اید. لطفاً بعداً دوباره امتحان کنید.",
        'status_code': status.HTTP_429_TOO_MANY_REQUESTS,
        'errors': [],
        'data': {}
    }

    USER_NOT_FOUND = {
        "code": "4006",
        "message": "کاربر یافت نشد.",
        'status_code': status.HTTP_404_NOT_FOUND,
        'errors': [],
        'data': {}
    }

    ACCOUNT_LOCKED = {
        "code": "4007",
        "message": "حساب شما به دلیل تلاش بیش از حد، موقتاً قفل شده است.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    AUTHENTICATION_FAILED = {
        "code": "4008",
        "message": "احراز هویت انجام نشد. لطفاً اطلاعات خود را بررسی کنید.",
        'status_code': status.HTTP_401_UNAUTHORIZED,
        'errors': [],
        'data': {}
    }

    MISSING_REQUIRED_FIELDS = {
        "code": "4009",
        "message": "برخی از فیلدهای ضروری ارسال نشده‌اند.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    INVALID_REQUEST = {
        "code": "4010",
        "message": "درخواست نامعتبر است.",
        'status_code': status.HTTP_400_BAD_REQUEST,
        'errors': [],
        'data': {}
    }

    OTP_NOT_EXPIRED = {
        "code": "4011",
        "message": "کد تأیید قبلی هنوز معتبر است. لطفاً پس از اتمام زمان اعتبار، درخواست جدید ارسال کنید.",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "errors": [],
        'data': {}
    }
    VERIFICATION_REQUEST_LIMIT_EXCEEDED = {
        "code": "4012",
        "message": "شما حد مجاز درخواست‌های کد تأیید را تکمیل کرده‌اید. لطفاً پس از مدتی دیگر مجدداً امتحان کنید.",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "errors": [],
        "data": {}
    }
    VERIFICATION_CODE_SENDING_FAILED = {
        "code": "4013",
        "message": "ارسال کد تأیید با خطا مواجه شد. لطفاً بعداً دوباره تلاش کنید.",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "errors": [],
        "data": {}
    }
    PHONE_NUMBER_REQUIRED = {
        "code": "4014",
        "message": "شماره تلفن همراه الزامی است.",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "errors": ["phone_number field is required."],
        "data": {}
    }
