

#
#
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
#
#
# def get_latest_verification_code(user):
#     # Get the latest verification code for a given user
#     return VerificationCode.objects.filter(user=user).order_by('-created_at').first()
#
#
# def check_verification_code(verification_code, verification_code_input, expected_code_type):
#     # Validate the provided verification code against the stored code
#     if not verification_code:
#         return Response(
#             {"message": "کد تأیید معتبری برای این کاربر وجود ندارد.", "data": None},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     # Check if the user is locked
#     if verification_code.is_locked():
#         return Response(
#             {"message": "شما به دلیل تلاش‌های ناموفق مکرر نمی‌توانید تا ۳۰ دقیقه دیگر کد تأیید جدیدی دریافت کنید.",
#              "data": None},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     # Check if the code type matches the expected type
#     if verification_code.code_type != expected_code_type:
#         return Response(
#             {"message": "نوع کد تأیید نادرست است.", "data": None},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     # Check if the code is still valid
#     if not verification_code.has_valid_code():
#         verification_code.is_valid = False
#         verification_code.save()
#         return Response(
#             {"message": "کد تأیید منقضی شده است.", "data": None},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     # Check if the number of failed attempts has reached the limit
#     if verification_code.failed_attempts >= FAILED_ATTEMPTS_LIMIT:
#         verification_code.is_valid = False
#         verification_code.lock_for(LOCKED_TIME_MINUTES)  # Lock the user for a specified period
#         verification_code.save()
#         return Response(
#             {"message": "شما بیش از حد مجاز تلاش کرده‌اید. کد تأیید غیر فعال شد و شما به مدت ۳۰ دقیقه قفل شدید.",
#              "data": None},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     # Check if the provided code matches the stored code
#     if verification_code_input != verification_code.random_code:
#         verification_code.failed_attempts += 1
#         if verification_code.failed_attempts >= FAILED_ATTEMPTS_LIMIT:
#             verification_code.lock_for(LOCKED_TIME_MINUTES)  # Lock the user for a specified period
#         verification_code.save()
#         return Response(
#             {"message": "کد تأیید اشتباه است.", "data": None},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     return None
#
#
# def process_verification_code_request(phone_number, code_type, user_type=None, is_registration=False):
#     # Check if user exists
#     user = User.objects.filter(phone_number=phone_number).first()
#
#     if not user and is_registration:
#         # Create or update user for registration
#         user = create_or_update_user({'phone_number': phone_number, 'user_type': user_type})
#     elif user:
#         if is_registration and user.is_active:
#             return None, "کاربری با این شماره تلفن از قبل ثبت ‌نام کرده است."
#
#         # Update user type if provided
#         if user_type and user.user_type != user_type:
#             user.user_type = user_type
#             user.save()
#
#     elif not user:
#         return None, "کاربری با این شماره تلفن یافت نشد."
#
#     # Create a new verification code using the model method
#     verification_code, error_message = VerificationCode.create_verification_code(user, code_type=code_type)
#
#     if verification_code:
#         # Send verification code via SMS
#         sms_response = send_registration_verification_code_sms(user.phone_number, verification_code.random_code)
#         if sms_response:
#             return {
#                 "message": "کد تأیید به شماره تلفن شما ارسال شد.",
#                 "data": {
#                     "verification_code_validity_seconds": VERIFICATION_CODE_VALIDITY_MINUTES * 60,
#                     "verification_code_length": VERIFICATION_CODE_LENGTH
#                 }
#             }, None
#         else:
#             verification_code.delete()  # If SMS fails, delete the verification code
#             return None, "مشکل در ارسال کد تأیید توسط سامانه."
#     else:
#         return None, error_message
