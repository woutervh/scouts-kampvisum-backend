from django.conf import settings
from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = settings.DEFAULT_PAGINATION_RESULTS
    max_page_size = settings.DEFAULT_PAGINATION_MAX_RESULTS
    page_query_param = "page"
    page_size_query_param = "page_size"
