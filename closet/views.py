from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import ClosetCreateSerializer, ClosetSerializer
from .serializers import ClothCreateSerializer, ClothSerializer
from .models import Closet, Cloth
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import logging

# Create your views here.
logging = logging.getLogger(__name__)


class ClosetCreateView(generics.CreateAPIView):
    """create closet"""
    queryset = Closet.objects.all()
    serializer_class = ClosetCreateSerializer

    def create(self, request, *args, **kwargs):
        res = Closet.objects.create(
            user=request.user,
            closet_name=request.data['closet_name'],
            description=request.data['description']
        )
        serializer = self.serializer_class(res)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClosetListView(generics.ListAPIView):
    """return closet list"""
    queryset = Closet.objects.select_related(
        'account').order_by('-created_at').all()
    serializer_class = ClosetSerializer

    def get(self, request):
        closet = Closet.objects.prefetch_related(
            'closet').filter(user=request.user)
        serializer = self.serializer_class(closet, many=True)
        return Response(serializer.data)

class ClosetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Closet.objects.select_related(
        'user').order_by('-created_at').all()
    serializer_class = ClosetSerializer

    def get(self, request, pk=None):
        instance = get_object_or_404(
            self.queryset, id=pk, user=request.user
        )
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(
            self.queryset, id=pk, user=request.user)
        instance.closet_name = request.data['closet_name']
        instance.description = request.data['description']
        instance.save()
        serializer = self.serializer_class(instance, partial=True)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        instance = get_object_or_404(
            self.queryset, id=pk, user=request.user
        )
        instance.delete()
        message = {'message':'クローゼットを削除しました'}
        return Response(message, status=status.HTTP_200_OK)

class ClosetAllDeleteView(generics.DestroyAPIView):
    queryset = Closet.objects.select_related('user').all()
    serializer_class = ClosetSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = get_list_or_404(self.queryset, user=request.user)
            instance.delete()
            data = {'message': '全てのクローゼットを削除しました'}
            return Response(data, status=status.HTTP_200_OK)
        except:
            error = {'message': 'クローゼットの削除に失敗しました'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

#ベーシック レンタルプラン用のcloth作成
class ClothBasicCreate(generics.CreateAPIView):
    queryset = Cloth.objects.select_related('closet', 'product').all()
    serializer_class = ClothCreateSerializer
    def create(self, request):
        data = request.data
        closet = data['closet']
        product_id = data['product']
        clothes = Cloth.objects.select_related('closet', 'product').filter(closet_id=closet)
        if len(clothes) < 3:
            for cloth in clothes:
                #closet内にclothが存在する
                if cloth.product.id == product_id:
                    message = {'message':'この商品はすでにクローゼット内にあります。'}
                    return Response(message, status=status.HTTP_409_CONFLICT)

            Cloth.objects.select_related('closet', 'product').create(
                product_id = product_id,
                closet_id = closet
            )

            message = {'message','アイテムを追加しました'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {'message': 'アイテムの保存が3つまで可能です'}
            return Response(message, status=status.HTTP_400_REQEUST)

#premiumプランようにclothを作成
class ClothPremiumCreate(generics.CreateAPIView):
    queryset = Cloth.objects.select_related('closet', 'product').all()
    serializer_class = ClothCreateSerializer


    def create(self, request):
        data = request.data
        closet = data['closet']
        product_id = data['product']
        clothes = get_list_or_404(self.queryset, closet_id=closet)
        if len(clothes) < 4:
            for cloth in clothes:
                if cloth.product.id == product_id:
                    message = {'message':'この商品はすでにクローゼット内にあります。'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)

            Cloth.objects.select_related('closet', 'product').create(
                product_id = product_id,
                closet_id = closet
            )

            message = {'message','アイテムを追加しました'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {'message': 'プレミアムプランはアイテムの保存が４つまで可能です'}
            return Response(message, status=status.HTTP_400_REQEUST)


class ClothListView(generics.ListAPIView):
    queryset = Cloth.objects.select_related('closet', 'product').all()
    serializer_class = ClothSerializer

    def get(self, request):
        clothes = get_list_or_404(
            self.queryset, closet=request.GET['closet_id'])
        serializer = self.serializer_class(clothes, many=True)
        return Response(serializer.data)


class ClothDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Cloth.objects.select_related('closet', 'product').all()
    serializer_class = ClothSerializer

    def delete(self, request, pk=None):
        instance = get_object_or_404(self.queryset, id=pk)
        instance.delete()
        message = {'message': '{}をクローゼットから削除しました'.format(
            instance.product.product_name)}
        return Response(message, status=status.HTTP_200_OK)
