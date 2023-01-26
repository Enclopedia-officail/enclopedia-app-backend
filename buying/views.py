from .models import Payment, Order, OrderItem
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from djago.shortcuts import get_object_or_404, get_list_or404

import stripe
import logging

logger = logging

#商品を買うために条件を満たす必要
#貸し出し中のアイテムであること
#返却期限が過ぎていないこと
#購入が確定した場合に返却しなくても問題がないことがわかるようにする
class BuyingReservationItemView(APIView):
    pass

