from unicodedata import category
from rest_framework.response import Response
from .serializers import CategorySerializer, BrandSerializer, TypeSerializer
from .models import Category, Brand, Type
from product.models import Product
from product.serailizers import ProductSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from product.serailizers import ProductSerializer
from django.shortcuts import get_list_or_404
from django.db.models import Q
import logging

# Create your views here.

# slugを利用してcateogryからマッチしたもの全て取り出すようにする
# tagとcategoryを合わせて使うかどうか
# slugフィールドに指定された値がurlの末尾に含まれている場合のproduct全てを作成日もしくは変更順に並び替えてから表示するようにする
# cateigoryからproduct逆参照を逆参照して取り出すようにする
logger = logging.getLogger(__name__)

# prefetch_related productをするかどうかs
class TypeListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = None

class CategoryListView(generics.ListAPIView):
    "get category list with id of type"
    permission_classes = (AllowAny,)
    queryset = Type.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get(self, request):
        try:
            id = request.GET['type']
            print(id)
            type = Type.objects.prefetch_related('type').get(id=id)
            categorys = type.type.all()
            print(categorys)
            serializer = self.serializer_class(categorys, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            data = {'message': 'アイテムを取得できませんでした'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

class CategorySearchListView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        instance = get_list_or_404(self.queryset)
        serializer = self.serializer_class(
            instance, many=True)
        return Response(serializer.data)


class CategorySearchView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get(self,   request, slug=None):
        category = Category.objects.get(slug=slug)
        products = category.products.order_by('-created_at').all()
        res = get_list_or_404(products)
        serializer = self.serializer_class(
            res, many=True)
        return Response(serializer.data)

#ブランドをアルファベットごとに取得するようにする
class BrandView(generics.ListAPIView):

    permission_classes = (AllowAny, )
    queryset = Brand.objects.order_by('brand_name').all()
    serializer_class = BrandSerializer

    def list(self, request):
        brand = get_list_or_404(
            self.queryset, brand_name__istartswith=request.query_params['brand'])
        serializer = self.serializer_class(
            brand, many=True)
        return Response(serializer.data)


class BrandSearchView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        brands = Brand.objects.get(slug=slug)
        products = brands.products.order_by('-created_at').all()
        res = get_list_or_404(products)
        serializer = self.serializer_class(
            res, many=True)

        return Response(serializer.data)

