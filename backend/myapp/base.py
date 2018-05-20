#coding=utf8
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 1000

class BaseView(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None
    search_fields = []
    permission_classes = []
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter]

    def perform_create(self, serializer):
        serializer.create(self.request.data)

    def perform_update(self, serializer):
        serializer.update(self.get_object(), self.request.data)

