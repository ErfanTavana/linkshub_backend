from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from linkshub_backend.core.utils import get_request_data


class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        data = get_request_data(request)
        phone_number = data.get('phone_number')


