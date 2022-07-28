from rest_framework.pagination import PageNumberPagination


class PaginationMobileProduct(PageNumberPagination):
    page_size = 8
    max_page_size = 100


class PaginationProduct(PageNumberPagination):
    page_size = 16
    max_page_size = 100