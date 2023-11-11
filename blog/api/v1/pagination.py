from rest_framework import pagination
from rest_framework.response import Response


class PostPagination(pagination.PageNumberPagination):
    page_size = 2
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)
