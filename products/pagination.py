from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class VendorPagination(PageNumberPagination):
    page_size = 1  # default items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "pagination": {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "success": "Fetched vendors successfully."
        })
