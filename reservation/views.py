from product.models import Product
from .models import Reservation, ReservationItem
from rest_framework.views import APIView
from .serializers import ReservationSerializer, ReservationItemSerializer, ResrevationListSerializer, ReservationShippingNumberSerializer, ReservationReturnShippingNumberSerializer
from .serializers import ReservationItemUserSerializer
from rest_framework import generics
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db import transaction
from rest_framework import pagination
from rest_framework import status
from datetime import datetime
from dateutil.relativedelta import relativedelta
from cart.models import CartItem, Cart
from subscription.models import StripeAccount
from rest_framework.permissions import AllowAny

import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.utils import timezone

def get_last_date(date):
    return date.replace(day=calendar.monthrange(date.year, date.month)[1])

class ReservationPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

class ReservationLatestDataView(generics.RetrieveAPIView):
    serializer_class = ResrevationListSerializer
    queryset = Reservation.objects.select_related(
        'user', 'adress'
    ).order_by('-reserved_start_date').all().prefetch_related('reservationitem_set')

    def get(self, request):
        user = request.user
        status_list = [1, 3, 4]
        reservation = get_list_or_404(self.queryset, user=user, status__in=status_list)
        serializer = self.serializer_class(reservation, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationListItemView(generics.ListAPIView):
    serializer_class = ResrevationListSerializer
    queryset = Reservation.objects.select_related(
        'user', 'adress'
    ).order_by('-reserved_start_date').all().prefetch_related('reservationitem_set')

    def get(self, request):
        user = request.user
        stripe_account = get_object_or_404(StripeAccount, user_id=user)
        today = timezone.now()
        status_list = [1, 2, 3, 4, 5]
        contract_date = None
        if stripe_account.update_date:
            contract_date = stripe_account.update_date
        else:
            contract_date = stripe_account.start_date
        reservations = get_list_or_404(self.queryset, user=user, status__in = status_list, reserved_start_date__range=[contract_date, today])
        serializer = self.serializer_class(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationRentalListView(generics.ListAPIView):
    """reservation history about rental plan"""
    serializer_class = ResrevationListSerializer
    queryset = Reservation.objects.select_related(
        'user', 'adress'
    ).order_by('-reserved_start_date').all().prefetch_related('reservationitem_set')
    #一ヶ月ごとのdataを取得するようにする
    def get(self, request):
        user = request.user
        month = request.GET['month']
        today = datetime.datetime.now()
        status_list = [1, 2, 3, 4, 5]
        if int(month) > 0:
            #userの指定した月のデータを取得を取得する用意する
            current_month = (today - relativedelta(months=month)).replace(day=1, hour=0, minute=0,second=0)
            last_day = get_last_date(current_month)
        else:
            current_month = today.replace(day=1, hour=0, minute=0,second=0)
            last_day = today
        #各月の初めから週末までのデータをrequestに応じて取得するよるようにする
        reservation = get_list_or_404(self.queryset, user=user,status__in = status_list, reserved_start_date__range=[current_month, last_day])
        serializer = self.serializer_class(reservation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationRentalHalfYearView(generics.ListAPIView):
    serializer_class = ResrevationListSerializer
    queryset = Reservation.objects.select_related(
        'user', 'adress'
    ).order_by('-reserved_start_date').all().prefetch_related('reservationitem_set')

    def get(self, request):
        user = request.user
        today = datetime.datetime.now()
        start_date = today - relativedelta(months=6)
        status_list = [1, 2, 3, 4, 5]
        reservations = get_list_or_404(self.queryset, user=user, status__in = status_list, reserved_start_date__range=[start_date, today])
        serializer = self.serializer_class(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.select_related('user', 'adress').order_by('-reserved_start_date').all()

    def get(self, request):
        user = request.user
        stripe_account = get_object_or_404(StripeAccount, user_id=user)
        contarct_date = None
        status_list = [1, 2, 3, 4, 5]
        if stripe_account.update_date:
            contarct_date = stripe_account.update_date
        else:
            contarct_date = stripe_account.start_date
        today = datetime.datetime.now()
        reservations = get_list_or_404(self.queryset, user=user, status__in = status_list, reserved_start_date__range=[contarct_date, today])
        serailzier = self.serializer_class(reservations, many=True)
        return Response(serailzier.data, status=status.HTTP_200_OK)

class ReservationItemView(generics.RetrieveAPIView):
    serializer_class = ReservationItemSerializer
    queryset = ReservationItem.objects.select_related('product', 'reservation').all()
    #itemがそん
    def get(self, request):
        reservation_id = request.GET['reservation_id']

        reservation_item = get_list_or_404(self.queryset, reservation_id=reservation_id)
        serializer = self.serializer_class(reservation_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationItemUserGet(generics.ListAPIView):
    """
    confirm if reservations data exists for post product review
    """
    serializer_class = ReservationItemUserSerializer
    queryset = Reservation.objects.select_related(
        'user', 'adress'
    ).order_by('-reserved_start_date').all().prefetch_related('reservationitem_set')

    def get(self, request):
        try:
            today = datetime.datetime.now()
            start_date = today - relativedelta(months=1)
            reservations = Reservation.objects.filter(user=request.user, status=5, reserved_start_date__range=[start_date, today])
            serializer = self.serializer_class(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ReservationCreateView(APIView):
    def post(self, request):
        data = request.data
        adress = data['address']
        #frontendから受け取るのではなくこちらで処理する必要がある
        reserved_end_date = data['reserved_end_date']
        plan = data['plan']
        constract_date = data['contract_date']
        cart = data['cart']
        user = request.user
        status_list = [1, 3, 4, 5]
        reservation = Reservation.objects.order_by('-reserved_start_date').select_related('user', 'adress').filter(
            user=user, reserved_start_date__gte=constract_date, status__in = status_list)
        subscription_user_info = StripeAccount.objects.select_related('user_id').get(user_id=user)
        if subscription_user_info.is_active & (subscription_user_info.plan == plan == 'basic'):
            create_reservation = Reservation.objects.create(
                user=user,
                adress_id=adress,
                status=0,
                plan=plan,
                reserved_end_date=reserved_end_date,
            )

            try:
                if len(reservation) > 4:
                    raise
                elif len(reservation) > 0:
                    if reservation[0].is_reserved is True:
                        raise
                    else:
                        cartitems = CartItem.objects.filter(cart_id=cart)
                        with transaction.atomic():

                            # productはlistで送られてくる
                            for cartitem in cartitems:
                                product = get_object_or_404(
                                    Product, id=cartitem.product.id)
                                product.stock -= cartitem.quantite
                                if product.stock >= 0:
                                    product.save()

                                else:
                                    data = {
                                        'title': '在庫がありません',
                                        'message': '現在オーダーした商品の{}の在庫がない状態です、商品詳細ページで商品の在庫数を確認してください。'.format(cartitem.product.product_name)
                                    }
                                    return Response(data, status=status.HTTP_200_OK)
                                reservation_item = ReservationItem.objects.create(
                                    reservation=create_reservation,
                                    product=cartitem.product,
                                    quantity=cartitem.quantite
                                )

                                if cartitem.variation.exists():
                                    reservation_item.variation.add(cartitem.variation)

                            create_reservation.status = 1
                            create_reservation.is_reserved = True
                            create_reservation.save(update_fields=["status","is_reserved"])
                            # 予約が完了するればカートを削除する
                            Cart.objects.get(user=user).delete()
                            data = {
                                'title': '予約が完了しました',
                                'message': '予約が完了しました,商品お届けまで3日ほどお時間をいただいております（天候等の影響により到着が遅れる場合がございます、ご了承ください.商品発送後に通知をいたします、到着まで今しばらくお待ちください'
                            }
                            return Response(data, status=status.HTTP_200_OK)
                else:
                    cartitems = CartItem.objects.filter(cart_id=cart)
                    # 処理に失敗すれば元に戻るようにする
                    with transaction.atomic():

                        # productはlistで送られてくる
                        for cartitem in cartitems:
                            product = get_object_or_404(
                                Product, id=cartitem.product.id)
                            product.stock -= cartitem.quantite
                            if product.stock >= 0:
                                product.save()

                            else:
                                data = {
                                    'title': '在庫がありません',
                                    'message': '現在オーダーした商品の{}の在庫がない状態です、商品詳細ページで商品の在庫数を確認してください。'.format(cartitem.product.product_name)
                                }
                                return Response(data, status=status.HTTP_200_OK)
                            reservation_item = ReservationItem.objects.create(
                                reservation=create_reservation,
                                product=cartitem.product,
                                quantity=cartitem.quantite
                            )

                            if cartitem.variation.exists():
                                reservation_item.variation.add(cartitem.variation)

                        # stutasをacceptedにする
                        create_reservation.status = 1
                        create_reservation.is_reserved = True
                        create_reservation.save(update_fields=["status","is_reserved"])
                        # 予約が完了するればカートを削除する
                        Cart.objects.get(user=user).delete()
                        data = {
                                'title': '予約が完了しました',
                                'message': '予約が完了しました,商品お届けまで3日ほどお時間をいただいております（天候等の影響により到着が遅れる場合がございます、ご了承ください.商品発送後に通知をいたします、到着まで今しばらくお待ちください'
                                }
                        return Response(data, status=status.HTTP_200_OK)
            except:
                cartitems = CartItem.objects.filter(cart_id=cart)
                for cartitem in cartitems:
                    product = Product.objects.select_related(
                        'brand', 'category', 'price').prefetch_related('tag').get(id=cartitem.product.id)
                    reservation_item = ReservationItem.objects.create(
                        reservation=create_reservation,
                        product=cartitem.product,
                        quantity=cartitem.quantite,
                    )
                    if cartitem.variation.exists():
                        reservation_item.variation.add(cartitem.variation)

                create_reservation.status = 2
                create_reservation.save(update_fields=["status"])
                Cart.objects.get(user=user).delete()
                error = {
                    'title': '商品の予約に失敗しました',
                    'message': '商品の予約に失敗しました、現在予約中の商品があるか在庫がない場合がございます'
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

        elif subscription_user_info.is_active & (subscription_user_info.plan == plan == 'premium'):
            #reservationがだった場合にはis_reserved参照errorが発生する
            try:
                if len(reservation) > 0:
                    if reservation[0].is_reserved == True:
                        message = {'message': '現在予約中の商品があります'}
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        create_reaservation = Reservation.objects.create(
                            user=user,
                            adress_id=adress,
                            status=0,
                            plan=plan,
                            reserved_end_date=reserved_end_date,
                        )
                        cartitems = CartItem.objects.filter(cart_id=cart)

                        # 処理に失敗すればdbを元に戻す
                        with transaction.atomic():
                            # productはlistになっている
                            for cartitem in cartitems:
                                product = Product.objects.select_related(
                                    'brand', 'category', 'price').prefetch_related('tag').get(id=cartitem.product.id)

                                product.stock -= cartitem.quantite
                                if product.stock >= 0:
                                    product.save()
                                else:
                                    data = {
                                        'title': '在庫がありません',
                                        'message': '現在オーダーした商品の{}の在庫がない状態です、商品詳細ページで商品の在庫数を確認してください。'.format(cartitem.product.product_name)
                                    }
                                    return Response(data, status=status.HTTP_200_OK)
                                reservation_item = ReservationItem.objects.create(
                                    reservation=create_reaservation,
                                    product=cartitem.product,
                                    quantity=cartitem.quantite,
                                )
                                if cartitem.variation.exists():
                                    reservation_item.variation.add(cartitem.variation)

                            create_reaservation.status = 1
                            create_reaservation.is_reserved = True
                            create_reaservation.save(update_fields=["status","is_reserved"])
                            Cart.objects.get(user=user).delete()
                        data = {
                                'title': '予約が完了しました',
                                'message': '予約が完了しました,商品お届けまで3日ほどお時間をいただいております（天候等の影響により到着が遅れる場合がございます、ご了承ください.商品発送後に通知をいたします、到着まで今しばらくお待ちください'
                                }
                        return Response(data, status=status.HTTP_200_OK)
                else:

                    create_reaservation = Reservation.objects.create(
                        user=user,
                        adress_id=adress,
                        status=0,
                        plan=plan,
                        reserved_end_date=reserved_end_date,
                    )
                    cartitems = CartItem.objects.filter(cart_id=cart)

                    # 処理に失敗すればdbを元に戻す
                    with transaction.atomic():
                        # productはlistになっている
                        for cartitem in cartitems:
                            product = get_object_or_404(
                                Product, id=cartitem.product.id)
                            product.stock -= cartitem.quantite
                            if product.stock >= 0:
                                product.save()
                            else:
                                data = {
                                    'title': '在庫がありません',
                                    'message': '現在オーダーした商品の{}の在庫がない状態です、商品詳細ページで商品の在庫数を確認してください。'.format(cartitem.product.product_name)
                                }
                                return Response(data, status=status.HTTP_200_OK)
                            reservation_item = ReservationItem.objects.create(
                                reservation=create_reaservation,
                                product=cartitem.product,
                                quantity=cartitem.quantite
                            )
                            if cartitem.variation.exists():
                                reservation_item.variation.add(cartitem.variation)

                        create_reaservation.status = 1
                        create_reaservation.is_reserved = True
                        create_reaservation.save(update_fields=["status","is_reserved"])
                        Cart.objects.get(user=user).delete()
                    data = {
                                'title': '予約が完了しました',
                                'message': '予約が完了しました,商品お届けまで3日ほどお時間をいただいております（天候等の影響により到着が遅れる場合がございます、ご了承ください.商品発送後に通知をいたします、到着まで今しばらくお待ちください'
                            }
                    return Response(data, status=status.HTTP_200_OK)
            except:
                with transaction.atomic():
                    reservation.status = 2
                    reservation.save()

                    for cartitem in cartitems:
                        product = Product.objects.select_related(
                            'brand', 'category', 'price').prefetch_related('tag').filter(id=cartitem['product'])
                        reservation_item = ReservationItem.objects.create(
                            reservation=create_reservation,
                            product=product,
                            quantity=cartitem.quantite,
                        )
                        if cartitem.variation.exists():
                            reservation_item.variation.add(cartitem.variation)
                error = {
                    'title': '商品の予約に失敗しました',
                    'message': '商品の予約に失敗しました、現在予約中の商品があるか在庫がない場合がございます'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {
                'title': '予約に失敗しました',
                'message': 'サブスクリプションプランに登録して下さい'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    # 予約した商品を一日以内であればキャンセルできるようにする。
    def update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        reservation_item_id = data.reservation_item
        today = datetime.datetime.now()

        # 個々のアイテムごとにキャンセルができるようにする
        reservation = get_list_or_404(Reservation, user_id=user)[0]
        reservation_items = get_list_or_404(
            ReservationItem, user_id=user, reservation=reservation.id)

        diff_date = reservation.reesrved_start_date - today
        if reservation.is_reserved == True:
            if diff_date <= 1:
                message = {'message': '予約から一日以上過ぎている商品に関してはキャンセルができません。'}
                return Response(message, status=status.HTTP_200_OK)
            # 日付が一日を超過している場合の処理
            else:
                # statusの状態をキャンセルにする
                for item in reservation_items:
                    if reservation_item_id == item.id:
                        # キャンセル指定した商品のみitemから削除を行うようにする
                        cancel_item = get_object_or_404(
                            ReservationItem, id=reservation_item_id)
                        cancel_item.is_canceled = True
                        # 現在時刻を指定
                        cancel_item.cancel_date = today
                        cancel_item.save()
                message = {'message': 'キャンセルが完了しました'}
                return Response(message, status=status.HTTP_200_OK)
        else:
            # 最初のreservatino_dateがtrueの場合はレンタル中の商品があるといることだがない場合の処理を記述
            message = {'message': '予約中の商品が存在しません'}
            return Response(message, sttus=status.HTTP_400_BAD_REQUEST)

#reservationのstatusの状態を変異発送が完了した場合
class ShippingNumberUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationShippingNumberSerializer

    def update(self, request, pk, *args, **kwargs):
        try:
            data = request.data
            instance = Reservation.objects.get(id=pk)
            instance.status = data['status']
            instance.shipping_number = data['shipping_number']
            instance.save(update_fields=["status","shipping_number"])
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
#商品返却時のview
class ReturnShippingNumberUpdateView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationReturnShippingNumberSerializer

#商品が返却されたことを確認後に行うview
class ReturnProductConfirmView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def update(self, request, pk, *args, **kwargs):
        data = request.data
        instance = get_object_or_404(Reservation, id=pk)
        instance.status = data['status']
        instance.save(update_fields=['status'])
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

#SHIPPINGの商品一覧を取得するAPI
class ShippingReservationsListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Reservation.objects.filter(status=4)
    serializer_class = ReservationSerializer

#返却が完了した時の処理
class CompleteRetrunView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def update(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Reservation, id=pk)
        instance.status = 5
        instance.is_reserved = False
        instance.return_date = datetime.datetime.now()
        instance.save(update_fields=['status','is_reserved','return_date'])
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetReservationItemView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = ReservationItem.objects.select_related('product', 'reservation').all()
    serializer_class = ReservationItemSerializer

    def get(self, request, pk):
        instance = get_object_or_404(ReservationItem, id=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
