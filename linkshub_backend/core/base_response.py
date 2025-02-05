from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class BaseResponse:
    @staticmethod
    def success(message="عملیات موفقیت‌آمیز بود.", data=None, status_code=status.HTTP_200_OK, code=1000, warnings=None,
                meta=None):
        return Response({
            "success": True,
            "code": code,
            "message": message,
            "data": data,
            "warnings": warnings,
            "meta": meta
        }, status=status_code)

    @staticmethod
    def error(message="خطایی رخ داده است.", errors=None, status_code=status.HTTP_400_BAD_REQUEST, code=2000, data=None):
        return Response({
            "success": False,
            "code": code,
            "message": message,
            "data": data,
            "errors": errors
        }, status=status_code)

    @staticmethod
    def paginate_queryset(queryset, request, serializer_class, message="عملیات موفقیت‌آمیز بود.",
                          status_code=status.HTTP_200_OK, code=1000, warnings=None, extra_data=None, data_key='items'):
        paginator = DefaultPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = serializer_class(paginated_queryset, many=True)

        response_data = {data_key: serializer.data}

        if extra_data:
            response_data.update({"extra_data": extra_data})

        meta = {
            "total_count": paginator.page.paginator.count,
            "total_pages": paginator.page.paginator.num_pages,
            "current_page": paginator.page.number,
            "page_size": paginator.get_page_size(request),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "first_page": 1,
            "last_page": paginator.page.paginator.num_pages,
            "timestamp": timezone.now(),
            "is_first_page": paginator.page.number == 1,
            "is_last_page": paginator.page.number == paginator.page.paginator.num_pages,
            "items_on_page": len(paginated_queryset),
            "has_more": paginator.page.has_next(),
        }

        return BaseResponse.success(message=message, data=response_data, status_code=status_code,
                                    code=code, warnings=warnings, meta=meta)
