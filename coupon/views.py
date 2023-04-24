from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Coupon, Issuing, Invitation, InvitationCode 
from .serializers import InvitationCodeSerializer, IssuingSerializer
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import datetime
import logging

#割引した料金を返す
class CouponDiscountView(APIView):
    queryset = Coupon.objects.all()

    def post(self, request):
        data = request.data
        coupon = get_object_or_404(self.queryset, id=data['coupon'])

        if coupon.amount_off != None:
            price = int(data['price']) - int(coupon.amount_off)
        elif coupon.percent_off != None:
            price = data['price'] - (data['price'] * coupon.percent_off)
        else:
            return Response(status=status.NOT_FOUND_404)
        data = {
            'price': price
        }
        return Response(data, status=status.HTTP_200_OK)

#couponを使用した際の処理
class UtilisedCouponView(APIView):
    queryset = Issuing.objects.select_related('user', 'coupon').all()
    def post(self, request):
        user = request.user
        data = request.data
        issuing = get_object_or_404(self.queryset, user=user, coupon__id=data['coupon'])
        coupon = issuing.coupon
        date = datetime.date.today()
        #使用回数の判定
        #ここの処理はクーポンを発行する際にする処理に変更する必要がある
        #クーポンの発行できる枚数を超過していないか確認する
        if coupon.redeem_by >= date:
            if coupon.duration == 'once':
                #使用回数は一回のみ
                #CouponとIssuingモデルの変更
                issuing.duration += 1
                issuing.is_used = True
                issuing.save()
                data = {
                    'message': 'クーポンを適用しました。'
                }
                return Response(data, status=status.HTTP_200_OK)
            elif coupon.duration ==  'repeting':
                issuing.duration += 1
                if issuing.duration == coupon.duration:
                    issuing.is_used = True
                    issuing.save()
                else:
                    issuing.save()
                data = {
                    'message': 'クーポンを適用しました。'
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                #制限なし
                issuing.duration += 1
                issuing.save()
                data = {
                    'message': 'クーポンを適用しました。'
                }
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'クーポンの有効期限が切れています'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

class InvitationCodeValidateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        phone_number_confirm = Invitation.objects.filter(phone_number=data['phone_number'])
        if phone_number_confirm.exists():
            data = {
                'message': '以前招待クーポンを受け取ったことのある方はご利用できません。'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                InvitationCode.objects.select_related('user').get(code=data['invitation_code'])
                return Response(status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                data = {
                    'message': '招待コードに誤りがあります,もう一度確認してから入力してください。'
                }
                return Response(data, status=status.HTTP_404_NOT_FOUND)

#招待した際にお互いにクーポンを発行する
#二度同様のemailあるいは電話番号を使用したログインの禁止
class InvitationView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        invitation_code = request.data['invitation_code']
        coupon = get_object_or_404(Coupon, name='友達招待クーポン')
        today = datetime.date.today()
        ninety_days_later = today + datetime.timedelta(days=90)
        try:
            invitation = InvitationCode.objects.select_related('user').get(code=invitation_code)
            issuings = []
            invited = Issuing(user=invitation.user, coupon=coupon, expiration=ninety_days_later)
            issuings.append(invited)
            is_invited = Issuing(user__phone_number=request.data['phone_number'], coupon=coupon, expiration=ninety_days_later)
            issuings.append(is_invited)
            Issuing.objects.bulk_create(issuings)
            coupon.times_redeemed += 2
            return Response(status=status.HTTP_200_OK)
        #招待コードが存在しなかった場合にはエラーが発生
        except ObjectDoesNotExist:
            data = {
                'title': '招待コードに誤りがあります。',
                'message': '招待コードに誤りがあります,もう一度確認してから入力してください。'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
#コードの獲得
class InvitationCodeGetView(generics.RetrieveAPIView):
    queryset = InvitationCode.objects.select_related('user').all()
    serializer_class = InvitationCodeSerializer

    def get(self, request):
        instance = get_object_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

#使用できるクーポンを一覧取得
class IssuingListView(generics.ListAPIView):
    queryset = Issuing.objects.select_related('user', 'coupon').all()
    serializer_class = IssuingSerializer

    #有効なIssuingを返す
    def get(self, request):
        type = request.GET['type']
        today = datetime.date.today()
        instance = get_list_or_404(self.queryset, user=request.user, expiration__gte=today, coupon__type=type)
        serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#登録した際に次回同様の情報を使用してクーポンの獲得ができないようにする
class CreateInvitationView(generics.CreateAPIView):
    queryset = Invitation.objects.select_related('InvitationCode').all()
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            Invitation.objects.create(InvitationCode__code=data['invitation_code'], phone_number=data['phone_number'])
            return Response(status=status.HTTP_200_OK)
        except ValidationError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    


        
