#coding=utf8
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer, UserSerializer, GroupSerializer
from .permissions import AuthOrReadOnly
from utils import DoubanBook, IdcData
from .base import BaseView
from .models import *

class DoubanApi(APIView):
    def get(self, request, **kwargs):
        name = kwargs.get('name')
        doubanbook = DoubanBook(name)
        data = doubanbook.get_detail()
        return Response({'data':data})

class IdcView(APIView):
    def get(self, request, **kwargs):
        data = IdcData().gettree()
        return Response({'data':data})

class BookViewSet(BaseView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AuthOrReadOnly, DjangoModelPermissions]
    search_fields = ['name', 'price', 'note']

class UserViewSet(BaseView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(BaseView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer