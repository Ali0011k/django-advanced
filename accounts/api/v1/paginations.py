from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserPagination(PageNumberPagination):
    """a pagination for user views"""

    page_size = 2
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)


class ProfilePagination(PageNumberPagination):
    """a pagination for profile views"""

    page_size = 2
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)
