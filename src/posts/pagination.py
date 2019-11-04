"""

Created by aditya on 28/3/19 at 1:01 PM

"""

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class PostPageNumberPagination(PageNumberPagination):
    page_size = 2
