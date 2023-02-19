from unicodedata import category
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, get_list_or_404
from category.models import Type
from .models import Product, Size, Variation, ImageGallary, ReviewRating, Tag
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from backend.pagination import BasicPagination
from . import serailizers
from reservation.models import Reservation
import re
import logging

logging.basicConfig(level=logging.DEBUG)
class ProductGetView(generics.RetrieveAPIView):
    """get the product detail"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').filter()
    serializer_class = serailizers.ProductDetailSerializer

    def get(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
        product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductSearch(generics.ListAPIView):
    """get products by search"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductSerializer
    pagination = BasicPagination

    def list(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            search_product = get_list_or_404(
            self.queryset, Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            pagination_product = self.paginate_queryset(search_product)
            serializer = self.serializer_class(
                pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
class ProductSearchReviewListView(generics.ListAPIView):
    """get products in highest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-review_count', '-rating').all()
    serailizer_class = serailizers.ProductSerializer

    def list(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(self.queryset, Q(
            product_name__icontains=keyword) | Q(description__iexact=keyword))
            pagination_product = self.paginate_queryset(products)
            serializer = self.serailizer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class ProductSearchReviewDescListView(generics.ListAPIView):
    """get products in lowest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('review_count', 'rating').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(self.queryset, Q(
            product_name__icontains=keyword) | Q(description__iexact=keyword))
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class ProductSearchFavoriteListView(generics.ListAPIView):
    """get products in order of number of favorites"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(self.queryset.annotate(
            Count('favorite_product')).order_by('-favorite_product__count', '-created_at'),
            Q(product_name__icontains=keyword) | Q(description__iexact=keyword))
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class ProductSearchFavoriteDescListView(generics.ListAPIView):
    """get products in order of least number of favorites"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(self.queryset.annotate(
            Count('favorite_product')).order_by('favorite_product__count', '-created_at'),
            Q(product_name__icontains=keyword) | Q(description__iexact=keyword))
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class ProductSearchOrderReservationView(generics.ListAPIView):
    """get products in order of number of reservations"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(self.queryset.annotate(
            Count('reservationitem')).order_by('-reservationitem__count', '-created_at'),
            Q(product_name__icontains=keyword) | Q(description__iexact=keyword))
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_404_NOT_FOUND)

#予約数の少ない順位並び替えを行う
class ProductSearchOrderReservationDescView(generics.ListAPIView):
    """get product in order of least number of reservations"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(self.queryset.annotate(
            Count('reservationitem')).order_by('reservationitem__count', '-created_at'),
            Q(product_name__icontains=keyword) | Q(description__iexact=keyword))
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_401_NOT_FOUND)

class ProductSearchPriceView(generics.ListAPIView):
    """get products in decreasing order of price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('price__price', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products =  get_list_or_404(
            self.queryset, Q(product_name__icontains=keyword) | Q(description__iexact=keyword), is_subscription__in=['rental', 'basic'])
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_401_NOT_FOUND)

class ProductSearchPriceDescView(generics.ListAPIView):
    """get products in descending order of price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-price__price', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            products = get_list_or_404(
            self.queryset, Q(product_name__icontains=keyword) | Q(description__iexact=keyword), is_subscription__in=['rental', 'basic'])
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            message = "検索キーワードが見当たりませんでした"
            return Response(message, status=status.HTTP_401_NOT_FOUND)
            
class ProductSearchCategoryListView(generics.ListAPIView):
    """get product for each category"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductCategoryListSerializer

    def list(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            category = request.GET['category']
            products = get_list_or_404(self.queryset, Q(
            product_name__icontains=keyword) | Q(description__iexact=keyword), category=category)
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)

class ProductSearchTypeListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['keyword']:
            keyword = request.GET['keyword']
            type = request.GET['type']
            type = Type.objects.prefetch_related('type').get(id=type)
            categorys = type.type.all()
            products = get_list_or_404(self.queryset, 
            Q(product_name__icontains=keyword) | Q(description__iexact=keyword),category__in=categorys)
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'キーワードを入力して下さい'}
            return Response(data, status=status.HTTP_200_OK)

class ProductTagListView(generics.ListAPIView):
    """get products for each tag"""
    permission_classes = (AllowAny, )
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        tag = request.GET['tag']
        product = get_list_or_404(self.queryset, tag__id=tag)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProudctTagRatingView(generics.ListAPIView):
    """get product in highest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-review_count', '-rating').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        tag = request.GET['tag']
        product = get_list_or_404(self.queryset, tag__id=tag)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductTagRatingDescView(generics.ListAPIView):
    """get product in lowest order of rating"""
    permission_classes = (AllowAny, )
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('review_count', 'rating').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        tag = request.GET['tag']
        product = get_list_or_404(self.queryset, tag__id=tag)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request}
        )
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductTagFavoriteView(generics.ListAPIView):
    """get product in order of most favorites"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        try:
            tag = request.GET['tag']
            product = get_list_or_404(self.queryset.annotate(
            Count('favorite_product')).order_by('-favorite_product__count', '-created_at'), tag__id=tag)
            pagination_product = self.paginate_queryset(product)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductTagReservationView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        try:
            tag = request.GET['tag']
            product = get_list_or_404(self.queryset.annotate(
            Count('reservationitem')).order_by('-reservationitem__count', '-created_at'),
            tag__id=tag
            )
            pagination_product = self.paginate_queryset(product)
            serializer = self.serializer_class(
                pagination_product, many=True, context={"request": request}
            )
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductTagReservationDescView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        try:
            tag = request.GET['tag']
            product = get_list_or_404(self.queryset.annotate(
            Count('reservationitem')).order_by('reservationitem__count', '-created_at'),
            tag__id=tag
            )
            pagination_product = self.paginate_queryset(product)
            serializer = self.serializer_class(
                pagination_product, many=True, context={"request": request}
            )
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductTagFavoriteDescView(generics.ListAPIView):
    """get product in order of least favorites"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def list(self, request):
        tag = request.GET['tag']
        product = get_list_or_404(self.queryset.annotate(
        Count('favorite_product')).order_by('favorite_product__count', '-created_at'), tag__id=tag)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductTagPriceOrderView(generics.ListAPIView):
    """get products in decreasing order of price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('price__price', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        try:
            tag = request.GET['tag']
            product = self.queryset.filter(tag__id=tag, is_subscription__in=['rental', 'basic'])
            pagination_product = self.paginate_queryset(product)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            message = '商品が取得できませんでした'
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class ProductTagPriceOrderDescView(generics.ListAPIView):
    """get products in decreasing order of price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-price__price', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        try:
            tag = request.GET['tag']
            product = self.queryset.filter(tag__id=tag, is_subscription__in=['rental', 'basic'])
            pagination_product = self.paginate_queryset(product)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            message = '商品が取得できませんでした'
            return Response(message, status=status.HTTP_404_NOT_FOUND)



class ProductTagCategoryView(generics.ListAPIView):
    """get products for each category"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductCategoryListSerializer

    def list(self, request):
        tag = request.GET['tag']
        category = request.GET['category']
        product = get_list_or_404(
        self.queryset, tag__id=tag, category=category)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductTagTypeView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        try:
            tag = request.GET['tag']
            type = request.GET['type']
            type = Type.objects.prefetch_related('type').get(id=type)
            categorys = type.type.all()
            products = get_list_or_404(
                self.queryset, tag__id=tag, category__in=categorys
            )
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            data = {'message': 'アイテムを取得できませんでした'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

#全ての商品を取得

class ProductListView(generics.ListAPIView):
    """get all products"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductSerializer
    pagination = BasicPagination

    def list(self, request):
        products = get_list_or_404(self.queryset)
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductReviewListView(generics.ListAPIView):
    """get product in highest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('-review_count', '-rating').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        product = get_list_or_404(self.queryset)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductReviewDescListView(generics.ListAPIView):
    """get product in lowest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').order_by('review_count', 'rating').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        product = get_list_or_404(self.queryset)
        pagination_product = self.paginate_queryset(product)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class FavoriteProductView(generics.ListAPIView):
    """get product in order of most favorites"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = self.queryset.annotate(
        Count('favorite_product')).order_by('-favorite_product__count', '-created_at')
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class FavoriteProductDescView(generics.ListAPIView):
    """get product in order of least favorites"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = self.queryset.annotate(
        Count('favorite_product')).order_by('favorite_product__count', '-created_at')
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductOrderReservationView(generics.RetrieveAPIView):
    """get products in order of number of reservations"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related('category', 'brand', 'price').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request, pk=None):
        products = self.queryset.annotate(
        Count('reservationitem')).order_by('-reservationitem__count', '-created_at')
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductOrderDescReservationView(generics.RetrieveAPIView):
    """get products in order of decreasing number of reservations"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request, pk=None):
        products = self.queryset.annotate(
        Count('reservationitem')).order_by('reservationitem__count', '-created_at')
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductPriceOrderView(generics.ListAPIView):
    """get products in decreasing order of price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('price__price').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = get_list_or_404(self.queryset, is_subscription__in=['rental', 'basic'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductPriceDescOrderView(generics.ListAPIView):
    """get products in descending order of price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-price__price').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = get_list_or_404(self.queryset, is_subscription__in=['rental', 'basic'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductCategoryView(generics.ListAPIView):
    """get product for each category"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductCategoryListSerializer
    lookup_field = 'category'

    def list(self, request, category=None):
        products = get_list_or_404(self.queryset, category=category)
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response((result.data))

class ProductTypeView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductSerializer
    def get(self, request):
        try:
            id = request.GET['type']
            type = Type.objects.prefetch_related('type').get(id=id)
            categorys = type.type.all()
            products = get_list_or_404(self.queryset, category__in=categorys)
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)
        except:
            data = {'message': 'アイテムを取得できませんでした'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


# brandから商品を取得するためのview

class ProductBrandView(generics.ListAPIView):
    """get product for each brand"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serializers_class = serailizers.ProductSerializer

    def list(self, request):
        products = get_list_or_404(
            self.queryset, brand_id=request.GET['brand'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializers_class(
            pagination_product, many=True, context={"request": request}
        )
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandReviewListView(generics.ListAPIView):
    """get product in highest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-review_count', '-rating').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = get_list_or_404(
        self.queryset, brand_id=request.GET['brand'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandReviewDescListView(generics.ListAPIView):
    """get product in lowest order of rating"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('review_count', 'rating').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = get_list_or_404(
        self.queryset, brand_id=request.GET['brand'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProducBrandFavoriteView(generics.ListAPIView):
    """get product in order of most favorite"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = get_list_or_404(self.queryset.annotate(
        Count('favorite_product')).order_by('-favorite_product__count', '-created_at'), brand_id=request.GET['brand'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)


class ProducBrandFavoriteDescView(generics.ListAPIView):
    """get product in order of least favorite"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        products = get_list_or_404(self.queryset.annotate(
        Count('favorite_product')).order_by('favorite_product__count', '-created_at'), brand_id=request.GET['brand'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandReservationView(generics.ListAPIView):
    """get products in order of number of reservations"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['brand']:
            brand = request.GET['brand']
            products = get_list_or_404(self.queryset.annotate(
            Count('reservationitem')).order_by('-reservationitem__count','-created_at'),
            brand=brand)
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandReservationDescView(generics.ListAPIView):
    """get products in order of decreasing number of reservations"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').all()
    serializer_class = serailizers.ProductSerializer

    def get(self,request):
        if request.GET['brand']:
            brand = request.GET['brand']
            products = get_list_or_404(self.queryset.annotate(
            Count('reservationitem')).order_by('reservationitem__count','-created_at'),
            brand=brand)
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request})
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandPriceView(generics.ListAPIView):
    """get products in order of lowest price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('price__price', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['brand']:
            brand = request.GET['brand']
            products = get_list_or_404(
            self.queryset, brand_id=brand, is_subscription__in=['rental', 'basic'])
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
                pagination_product, many=True, context={"request": request}
            )
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandPriceDescView(generics.ListAPIView):
    """get products in order of lowest price"""
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-price__price', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        if request.GET['brand']:
            brand = request.GET['brand']
            products = get_list_or_404(
            self.queryset, brand_id=brand, is_subscription__in=['rental', 'basic'])
            pagination_product = self.paginate_queryset(products)
            serializer = self.serializer_class(
                pagination_product, many=True, context={"request": request}
            )
            result = self.get_paginated_response(serializer.data)
            return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandCategoryView(generics.ListAPIView):
    """get brand products for each category"""
    permission_classes = (AllowAny, )
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serailizer_class = serailizers.ProductCategoryListSerializer

    def get(self, request):
        products = get_list_or_404(
        self.queryset, brand_id=request.GET['brand'],
        category_id=request.GET['category'])
        pagination_product = self.paginate_queryset(products)
        serializer = self.serailizer_class(
        pagination_product, many=True, context={"request": request})
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductBrandTypeView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
        'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('-created_at').all()
    serializer_class = serailizers.ProductCategoryListSerializer

    def get(self, request):
        brand = request.GET['brand']
        type = request.GET['type']
        type = Type.objects.prefetch_related('type').get(id=type)
        categorys = type.type.all()
        products = get_list_or_404(
            self.queryset, brand_id=brand, category__in=categorys
        )
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(
            pagination_product, many=True, context={"request": request}
        )
        result = self.get_paginated_response(serializer.data)
        return Response(result.data, status=status.HTTP_200_OK)

class ProductSizeView(generics.ListAPIView):
    """retrieve size of product"""
    permission_classes = (AllowAny,)
    queryset = Size.objects.select_related(
    'product').all()
    serializer_class = serailizers.SizeSerializer
    lookup_field = 'product'

    def list(self, request, product=None):
        size = get_list_or_404(self.queryset, product=product)
        serializer = self.serializer_class(size, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# tagからproductを取得する
class ProductTagView(generics.ListAPIView):
    """retrieve products from tag"""
    permission_classes = (AllowAny,)
    queryset = Tag.objects.select_related(
    'products').all()
    serailizers_class = serailizers.ProductSerializer

    def list(self, request):
        tag = get_list_or_404(self.queryset, tag_name=request.GET['tag'])
        products = tag.products.order_by('-created_at').all()
        res = get_list_or_404(products)
        serializer = self.serailizers_class(
        res, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

#関連商品を取得するためのapi
class RelatedProductListViwe(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').order_by('review_count', 'rating', '-created_at').all()
    serializer_class = serailizers.ProductSerializer

    def get(self, request):
        product = request.GET['product']
        product_info = get_object_or_404(self.queryset, id=product)
        products = get_list_or_404(self.queryset, brand=product_info.brand, category=product_info.category, stock__gte=1)
        serializer = self.serializer_class(products[:10], many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class VariationGetView(generics.ListAPIView):
    """retrieve variations of product"""
    permission_classes = (AllowAny,)
    queryset = Variation.objects.select_related(
    'product').all()
    serializer_class = serailizers.VariationSerialzier
    lookup_field = 'product'

    def list(self, request, product=None):
        variation = get_list_or_404(self.queryset, product=product)
        serializer = self.serializer_class(variation, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ImageGallaryView(generics.ListAPIView):
    """get images of product"""
    permission_classes = (AllowAny,)
    queryset = ImageGallary.objects.select_related(
    'product').all()
    serializer_class = serailizers.ImageGallarySerializer
    lookup_field = 'product'

    def list(self, request, product):
        images = get_list_or_404(self.queryset, product=product)
        serializer = self.serializer_class(
        images, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewRatingCreateView(generics.CreateAPIView):
    """create review against the product"""
    queryset = ReviewRating.objects.select_related(
    'account', 'product').all()
    serializer_class = serailizers.ReviewRatingSerializer
    lookup_field = 'product'

    def create(self, request, product):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            client_addr = ip.split(',')[0]
        else:
            client_addr = request.META.get('REMOTE_ADDR')
        reservation = get_list_or_404(Reservation, user=request.user, reservationitem__product_id=product)
        if len(reservation) > 0:
            res = ReviewRating.objects.select_related('account', 'product').create(
                user=request.user,
                product_id=product,
                title=request.data['title'],
                review=request.data['review'],
                rating=request.data['rating'],
                ip=str(client_addr)
            )
            serializer = self.serializer_class(res)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            message = {'message':'レンタルしたことがないアイテムに口コミ投稿することはできません。'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class ReviewList(generics.ListAPIView):
    """各プロダクトのレビューを全て取得"""
    permission_classes = (AllowAny,)
    queryset = ReviewRating.objects.select_related(
        'product', 'user'
    ).order_by('-on_created').all()
    serializer_class = serailizers.ReviewListSerializer
    lookup_field = "product"

    def get(self, request, product=None):
        try:
            reviews = get_list_or_404(self.queryset, product=product)
            serializer = self.serializer_class(
            reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            message="レビューがありません"
            return Response(message, status=status.HTTP_404_NOT_FOUND)


# reviewをproductごとにリストで取得
class ReviewRatingView(generics.ListAPIView):
    """プロダクトを個数制限をかけて取得する"""
    permission_classes = (AllowAny,)
    queryset = ReviewRating.objects.select_related(
    'product', 'user').order_by('-on_created').all()
    serializer_class = serailizers.ReviewListSerializer
    lookup_field = 'product'
    def list(self, request, product=None):
        try:
            reviews = get_list_or_404(self.queryset, product=product)
            serializer = self.serializer_class(
            reviews[:3], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            message="レビューがありません"
            return Response(message, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, product=None):
        reviews = get_list_or_404(self.queryset, product=product)
        serializer = self.serializer_class(
        reviews[:3], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserReview(generics.RetrieveUpdateDestroyAPIView):
    """update review for each user"""
    queryset = ReviewRating.objects.select_related(
    'product', 'user').order_by('-on_created').all()
    serializer_class = serailizers.UserReviewSerializer

    def get(self, request, pk):
        review = get_object_or_404(ReviewRating,
        pk=pk)
        serializer = self.serializer_class(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        review = get_object_or_404(ReviewRating, pk=pk)
        review.delete()
        return Response('Your Review was deleted', status=status.HTTP_200_OK)

from .searchWrodData import word_list
import jaconv
class SearchWordView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        data = request.GET['word']
        if data:
            p = re.compile('[\u3041-\u309F]+')
            if p.match(data):
                word = jaconv.hira2kata(data)
                re_match = [w for w in word_list if re.match(word, w.lower())]
                return Response(re_match, status=status.HTTP_200_OK)
            else:
                lower_word = data.lower()
                re_match = [w for w in word_list if re.match(lower_word, w.lower())]
                return Response(re_match, status=status.HTTP_200_OK)
        else:
            #現在人気のワードを取得して格納する
            data = []
            return Response(data, status=status.HTTP_200_OK)

#文字からtagを複数取得
class TagListAPIVIew(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serailizers.TagSerializer
    queryset = Tag.objects.all()

    def get(self, request):
        data = request.GET['tag']
        instance = get_list_or_404(self.queryset, tag_name__icontains=data)
        serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#複数指定したタグからproductを取得
class TagListProductGetView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serailizers.ProductSerializer
    queryset = Product.objects.select_related(
    'category', 'brand', 'price'
    ).prefetch_related('tag').all()

    def get(self, request):
        tags = request.query_params.getlist('tags[]')
        products = self.queryset
        for id in tags:
            products = products.filter(tag__id=id)
        pagination_product = self.paginate_queryset(products)
        serializer = self.serializer_class(pagination_product, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)