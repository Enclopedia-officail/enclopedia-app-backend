from .models import Payment, Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from djago.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment, Order, OrderItem
from subscription.models import StripeAccount
from reservation.models import ReservationItem

import stripe
import logging

logger = logging.basicConfig(level=logging.DEBUG)
#商品を買うために条件を満たす必要
#貸し出し中のアイテムであること
#返却期限が過ぎていないこと
#購入が確定した場合に返却しなくても問題がないことがわかるようにする

def create_payment(user, payment_method, payment_id):
    instance = Payment.objects.select_related('order_account').create(user=user)
    return instance


class BuyingReservationItemView(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        stripe_customer = StripeAccount.objects.select_related('user_id').get(user_id=user)
        response = stripe.PaymentIntent.create(
            customer = stripe_customer,
            payment_method_types=data['payment_method'],
            payment_method = data['payment_id'],
            currency="jpy",
            amount=data['total_price'],
            confirm=True
        )
        instance = get_object_or_404(Order.objects.select_related(
            'order_account', 'order_address', 'order_payment'),
            id = data['order_id']
            )
        if response.data['status'] == 'succeded':
            #支払いが成功した場合
            instance.status = 'Completed'
            instance.save(update_fields=['status', 'updated_at'])
            message = {
                'message': '商品の購入が完了しました'
            }
            return Response(message, status=status.HTTP_200_OK)
        elif response.data['status'] == 'requires_payment_method':
            #支払いが失敗した場合の処理
            instance.status = 'Cancelled'
            instance.save(update_fields=['status', 'updated_at'])
            error = {
            'message': '支払いに失敗しました。'
            }
            return Response(error, status=status.HTTP_404_NOT_FOUND)

class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.select_related('order_item_account', 'order_item').all()
    serializer_class = OrderItemSerializer

    def get(self, request):
        instance = get_list_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.select_related('order_item_account', 'order_payment', 'order_item').all()
    serializer_class = OrderItemSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        instance = OrderItem.objects.select_related('order_item_account', 'order_payment', 'order_item').create(
            user = user,
            order__id = data['order_id'],
            reservation_item__id = data['reservation_item_id'],
            quantity = data['quantity'],
            is_ordered = True
        )
        serializer = self.serializer_class(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OrderCreateView(generics.CreateAPIView):

    queryset = Order.objects.select_related('order_account', 'order_address').all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        instance = Order.objects.select_related('order_account', 'order_address').create(
            user = request.user,
            address__id = data['address'],
            order_id = data['order_id'],
            total_price = data['total_price'],
            tax = data['tax'],
            status = 'Accepted',
            ip = "requestからipを首藤",
        )
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.select_related('payment_account').all()
    serializer_class = PaymentSerializer

    def  post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        instance = Payment.objects.select_related('payment_account').create(
            user = user,
            payment_method =  data['payment_met,hod'],
            payment_id = data['payment_id'],
            amount_paid = data['amount_paid']
        )
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    