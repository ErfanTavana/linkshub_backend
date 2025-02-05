from rest_framework.response import Response
from rest_framework import status


class BaseResponse:
    @staticmethod
    def success(
            message="عملیات موفقیت‌آمیز بود.",
            data=None,
            status_code=status.HTTP_200_OK,
            code=1000,
            warnings=None,
            meta=None
    ):
        return Response({
            "success": True,
            "code": code,
            "message": message,
            "data": data,
            "warnings": warnings,
            "meta": meta
        }, status=status_code)

    @staticmethod
    def error(
            message="خطایی رخ داده است.",
            errors=None,
            status_code=status.HTTP_400_BAD_REQUEST,
            code=2000
    ):
        return Response({
            "success": False,
            "code": code,
            "message": message,
            "errors": errors
        }, status=status_code)
