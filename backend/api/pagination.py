from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class SubPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'recipes_limit'
