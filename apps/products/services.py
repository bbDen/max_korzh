from rest_framework.pagination import PageNumberPagination


class PaginationProduct(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'limit'
    max_page_size = 16


