from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from linkshub_backend.core.utils import get_request_data
from accounts.services.auth_otp_service import send_otp
from linkshub_backend.core.error_codes import ErrorCodes
from linkshub_backend.core.base_response import BaseResponse
class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        data = get_request_data(request)
        phone_number = data.get('phone_number')

        if not phone_number:
            return BaseResponse.error(
                message=ErrorCodes.PHONE_NUMBER_REQUIRED["message"],
                errors=ErrorCodes.PHONE_NUMBER_REQUIRED["errors"],
                code=ErrorCodes.PHONE_NUMBER_REQUIRED["code"],
                status_code=ErrorCodes.PHONE_NUMBER_REQUIRED["status_code"]
            )
        ip_address = request.META.get('REMOTE_ADDR')

        result = send_otp(phone_number=phone_number, ip_address=ip_address)

        return Response(result, status=status.HTTP_200_OK)