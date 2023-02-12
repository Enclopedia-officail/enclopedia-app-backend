from .models import Payment, Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404
from subscription.models import StripeAccount

import stripe
import logging

import string
import random

logger = logging.basicConfig(level=logging.DEBUG)
#商品を買うために条件を満たす必要
#貸し出し中のアイテムであること
#返却期限が過ぎていないこと
#購入が確定した場合に返却しなくても問題がないことがわかるようにする

class BuyingReservationItemView(APIView):
    #ユーザが見やすい一意の予約番号を発行する
    #人にわかりやすい予約番号を重複せずに発行する方法を考える
    #数字大文字小文字からランダムに１１桁の数値を作成する

    def payment(self, data, customer):
        response = stripe.PaymentIntent.create(
            customer = customer,
            payment_method_types=['card'],
            payment_method = data['payment_id'],
            currency="jpy",
            amount=data['total_price'],
            confirm=True
        )
        return response

    def post(self, request):
        data = request.data
        user = request.user
        stripe_customer = StripeAccount.objects.select_related('user_id').get(user_id=user)
        response = self.payment(data, stripe_customer.customer_id)
        instance = get_object_or_404(Order.objects.select_related('user', 'payment'), id = data['order_id'])
        if response['status'] == 'succeeded':
            #支払いが成功した場合
            instance.status = 'Completed'
            instance.payment_intent_id = response['id']
            instance.save(update_fields=['status', 'payment_intent_id'])
            message = {
                'message': '商品の購入が完了しました'
            }
            return Response(message, status=status.HTTP_200_OK)
        elif response['status'] == 'requires_payment_method':
            #支払いが失敗した場合の処理
            instance.status = 'Cancelled'
            instance.payment_intent_id = response['id']
            instance.save(update_fields=['status', 'payment_intent_id'])
            error = {'message': '支払いに失敗しました。'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {'message': '支払いを受付に失敗しました。'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

class OrderItemGetView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.select_related('user', 'order', 'reservation_item').all()
    serializer_class = OrderItemSerializer

    def get(self, request, pk):
        instance = get_object_or_404(self.queryset, id=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.select_related('user', 'order', 'reservation_item').all()
    serializer_class = OrderItemSerializer

    def get(self, request):
        instance = get_list_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.select_related('user', 'order', 'reservation_item').all()
    serializer_class = OrderItemSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        instance = OrderItem.objects.select_related('user', 'order', 'reservation_item').create(
            user = user,
            order_id = data['order_id'],
            reservation_item_id = data['reservation_item_id'],
            is_ordered = True
        )
        reservation_item = instance.reservation_item
        reservation_item.is_bought = True
        reservation_item.save()
        serializer = self.serializer_class(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderCreateView(generics.CreateAPIView):

    queryset = Order.objects.select_related('order_account', 'order_address').all()
    serializer_class = OrderSerializer

    def get_reservation_number(self, length):
        letters = string.ascii_letters
        number = string.digits
        num = ''.join(random.choice(letters + number) for i in range(length))
        return num

    def post(self, request, *args, **kwargs):
        data = request.data
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            client_ip = ip_address.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        instance = Order.objects.select_related('order_account', 'order_address').create(
            user = request.user,
            payment_id = data['payment'],
            order_id = self.get_reservation_number(11),
            total_price = data['total_price'],
            tax = data['tax'],
            status = 'Accepted',
            ip = client_ip
        )
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.select_related('payment_account').all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        print(data['payment_method'])
        instance = Payment.objects.select_related('payment_account').create(
            user = user,
            payment_method = data['payment_method'],
            payment_id = data['payment_id'],
        )
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    