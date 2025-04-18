from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def generate_pagination_response(self, data, message):
    return Response({
        "data": data,
        "pagination": {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link()
        },
        "success": f"{message}"
    })


class VendorPagination(PageNumberPagination):
    page_size = 2  # default items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return generate_pagination_response(self=self, data=data, message='Fetched vendors successfully.')


class ProductPagination(PageNumberPagination):
    page_size = 2  # default items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return generate_pagination_response(self=self, data=data, message='Fetched Product successfully.')
