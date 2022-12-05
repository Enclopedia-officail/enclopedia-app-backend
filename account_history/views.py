from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Favorite
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import FavoriteSerialzier, FavoriteListSerializer
from product.models import Product
from product.serailizers import ProductSerializer
from rest_framework import status
import environ
import logging

logging.basicConfig(level=logging.DEBUG)

env = environ.Env()

# Create your views here.

# お気に入りに関する処理
# get create updateからなる、filterを使用してuserのお気に入りを全て取得、
# cacheに保存しておきcreate、deleteの場合にのみ更新、cacheにデータが存在する限りはget requestを行わないようにする


class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerialzier

    def create(self, request):
        try:
            favorites = Favorite.objects.filter(user=request.user)
            if len(favorites) == 0:
                res = Favorite.objects.create(
                    user=request.user, product_id=request.data['product'])
                serializer = self.serializer_class(res)
                return Response(serializer.data)
            else:
                for favorite in favorites:
                    if str(favorite.product.id) == str(request.data['product']):
                        message = '既にお気に入りに追加してある商品です'
                        return Response(message, status.HTTP_409_CONFLICT)

                res = Favorite.objects.create(
                    user=request.user, product_id=request.data['product'])
                serializer = self.serializer_class(res)
                return Response(serializer.data)
        except:
            message={'message': 'お気に入りに追加できませんでした。'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)


class FavoriteGetView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Favorite.objects.select_related('user', 'product').all()
    serializer_class = FavoriteSerialzier

    def retrieve(self, request):
        product = request.GET['product']
        product = get_object_or_404(self.queryset, product_id=product)
        serializer = self.serializer_class(product)
        return Response(serializer.data)


class FavoriteListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Favorite.objects.select_related(
        'product', 'user').order_by('-created_at').all()
    serializer_class = FavoriteListSerializer

    def list(self, request):
        favorites = get_list_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(
            favorites, many=True)
        return Response(serializer.data)

class FavoriteDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerialzier

    def delete(self, request, pk=None):
        favorite = get_object_or_404(Favorite, pk=pk)
        favorite.delete()
        message = 'お気に入りから削除しました'
        return Response(message, status=status.HTTP_200_OK)

import redis

def byte_to_str(byte_list: list) -> list:
    return [i.decode('utf8') for i in byte_list]

class BrowsingHistoryView(APIView):
    redisClient = redis.StrictRedis(host=env("REDIS_LOCATION"), port=6379, db=0)
    def get(self, request):
        try:
            user = request.user
            products_id = byte_to_str(list(self.redisClient.smembers(str(user.id))))
            products = Product.objects.select_related(
            'category', 'brand', 'price').prefetch_related('tag').filter(id__in=products_id)
            serializer = ProductSerializer(products, many=True)
            if products.count() < 30:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data[0:29], status=status.HTTP_200_OK)
                
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self, request):
        #userごとに履歴を作成できるようにする方法をとる
        #検索履歴に対しても保存ができるようにする
        try:
            product_id = request.data['product_id']
            user = request.user
            self.redisClient.sadd(str(user.id), product_id)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SearchHistoryView(APIView):
    redisClient = redis.StrictRedis(host=env('REDIS_LOCATION'), port=6379, db=0)
    def get(self, request):

            user = request.user
            data = byte_to_str(list(self.redisClient.smembers(str(user.id) + 'search')))
            if len(data) < 15:
                return Response(data, status=status.HTTP_200_OK)

            else:
                return Response(data[0:14], status=status.HTTP_200_OK)


    def post(self, request):
        try:
            search_word = request.data['search_word']
            user = request.user
            self.redisClient.sadd(str(user.id) + 'search', search_word)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
