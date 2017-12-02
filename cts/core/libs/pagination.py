from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.STANDARD_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = 1000
