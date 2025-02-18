import os
from dotenv import load_dotenv

load_dotenv()

# OTP Settings
# ==============================
OTP_API_KEY = os.getenv("OTP_API_KEY", "default_api_key_here")
OTP_VALIDITY_MINUTES = int(os.getenv("OTP_VALIDITY_MINUTES", 2))
OTP_SMS_TEMPLATE = str(os.getenv("OTP_SMS_TEMPLATE", ''))
OTP_LENGTH = int(os.getenv("OTP_LENGTH", 4))
OTP_REQUEST_LIMIT_HOURS = int(os.getenv("OTP_REQUEST_LIMIT_HOURS", 24))
OTP_REQUEST_LIMIT = int(os.getenv("OTP_REQUEST_LIMIT", 24))
OTP_LOCKED_TIME_MINUTES = int(os.getenv("OTP_LOCKED_TIME_MINUTES", 30))
OTP_FAILED_ATTEMPTS_LIMIT = int(os.getenv("OTP_FAILED_ATTEMPTS_LIMIT", 8))
# ==============================
