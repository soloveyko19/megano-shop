from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatalogPagination(PageNumberPagination):
    max_page_size = 100
    page_size = 20
    page_query_param = "currentPage"
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response(
            {
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
                "items": data,
            }
        )
