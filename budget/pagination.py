from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Page through results, letting clients ask for up to 100 per page."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
