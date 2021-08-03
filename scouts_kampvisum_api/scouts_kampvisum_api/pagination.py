from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 1000
    page_query_param = 'page'
    page_size_query_param = 'page_size'
