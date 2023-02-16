from rest_framework.pagination import (
    PageNumberPagination
)

from rest_framework.response import Response

class BasicPagination(PageNumberPagination):
    page_size = 40
    count_local = 0
    max_page_size = 40

    def __init__(self):
        super().__init__()

    def paginate_queryset(self, queryset, request, view=None):
        self.count_local = len(queryset)
        return super().paginate_queryset(queryset, request, view)

    #count部分をlenで表示するようにする
    def get_paginated_response(self, data):
        return Response({
            'count':self.count_local,
            'page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })