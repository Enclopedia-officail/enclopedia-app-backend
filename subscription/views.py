from cart.models import CartItem, Cart
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import StripeAccount
from product.models import Product
from reservation.models import Reservation, ReservationItem
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import StripeSubscriptionSerializer
from django.utils import timezone
import datetime
import environ
import stripe
import logging

#notification
from . import tasks


logging = logging.basicConfig(level=logging.DEBUG)
env = environ.Env()

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = '2020-08-27'

stripe.set_app_info(
    'stripe-samples/subscription-use-cases/fixed-price',
    version='0.0.1',
    url='https://github.com/sttipe-samples/subscription-use-cases/fixed-price')

# stripeに登録したサブスクリプションプラン料金表を返すようにする。

# subscriptionプランに関して


class StripeConfigView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        prices = stripe.Price.list(
            limit=2
        )
        return Response(prices.data)


class StripeAccountView(APIView):
    #アカウントがemail情報などを変えた時にこちらも更新をする
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            customer = StripeAccount.objects.get(user_id=request.user)
            stripe.Customer.modify(customer.customer_id, email=data['email'])
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    #アカウントを削除する際にstripeに登録したCustomerも削除する
    def delete(self, request, *args, **kwargs):
        try:
            stripe_account = get_object_or_404(StripeAccount, user_id=request.user)
            stripe.Customer.delete(stripe_account.customer_id)
            data = {"message": "stripeアカウントを完全に削除しました"}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_200_OK)


class StripeCustomerView(APIView):
    """enclopedia subscription function"""
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            stripe_info = StripeAccount.objects.get(
                user_id=request.user)
            if stripe_info:
                customer_info = stripe.Subscription.list(
                    customer=stripe_info.customer_id).data

                return Response(customer_info, status=status.HTTP_200_OK)
            else:
                raise
            
        except:
            message = {'message': 'サブスクリプションプランに登録していません'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        data = request.data
        email = data['email']
        payment_method = request.data['payment_method_id']
        subscription_plan = request.data['plan']
        price_id = request.data['price_id'].split('&')[0]
        customer_data = stripe.Customer.list(email=email).data
        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                email=email,
                payment_method=payment_method,
                invoice_settings={
                    'default_payment_method': payment_method,
                },
            )
        else:
            customer = customer_data[0]
        try:
            stripe_subscription = stripe.Subscription.create(
                customer=customer['id'],
                items=[
                    {
                        "price": price_id,
                    },
                ],
                expand=['latest_invoice.payment_intent'],
            )
            if stripe_subscription['status'] == 'active':
                # database stripeinfoを更新するようにする。

                stripe_info = StripeAccount.objects.get(
                    user_id=request.user)

                if stripe_info:
                    stripe_info.customer_id = customer['id']
                    stripe_info.is_active = True
                    stripe_info.plan_id = price_id
                    stripe_info.plan = subscription_plan
                    stripe_info.start_date = timezone.now()
                    stripe_info.save(update_fields=["customer_id", "is_active", "plan_id", "plan", "start_date"])
                    data = {
                        'title': 'サブスクリプションの登録が完了しました',
                        'message': 'この度はEnclopediaファッションレンタルサービスサブスクリプションへのご登録ありがとうございます、サブスクリプション{}プランへの登録が完了しました。'.format(subscription_plan)
                        }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    # サブスクリプションアカウントを登録します
                    StripeAccount.objects.create(
                        user_id=request.user,
                        is_active=True,
                        plan=subscription_plan,
                        plan_id=price_id,
                        start_date=timezone.now()
                    )
                    data = {
                        'title': 'サブスクリプションの登録が完了しました',
                        'message': 'この度はEnclopediaファッションレンタルサービスサブスクリプションへのご登録ありがとうございます、サブスクリプション{}プランへの登録が完了しました。'.format(subscription_plan)
                        }
                    return Response(data, status=status.HTTP_200_OK)
    
            elif stripe_subscription.latest_invoice.payment_intent.status == 'requires_payment_method':
                data = {
                    'title':'支払いに失敗しました',
                    'message':'支払いが受付けられませんでした、カード情報を更新の上再度支払いをして下さい 。'
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            message = {
                'title': '登録に失敗しました',
                'message': 'サブスクリプションの登録に失敗しました、再度登録を行なって下さい。',
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        #この更新方法だとinvoiceが作成されないので請求ができない
        user = request.user
        data = request.data
        price_id = data['price_id']
        customer = StripeAccount.objects.get(user_id=user)
        if customer:
            try:
                if customer.plan == 'basic':
                    subscription_info = stripe.Subscription.list(
                    customer=customer.customer_id,
                    status='active'
                    )
                    subscription_update = stripe.Subscription.modify(
                    subscription_info['data'][0].id,
                    items=[
                        {
                            "price": price_id,
                        },
                    ],)

                    stripe.SubscriptionItem.delete(
                        subscription_info['data'][0]['items']['data'][0].id,
                        proration_behavior="none"
                        )
                    #元のitemを削除後にsubscriptionアップデートプランに加入する

                    customer.price_id = price_id
                    customer.plan = data['plan']
                    update_date = datetime.datetime.fromtimestamp(subscription_update.start_date)
                    customer.update_date = update_date
                    customer.save(update_fields=["plan", 'update_date'])
                    date = customer.update_date.strftime('%Y年%m月%d日')
                    data = {
                        'title': 'サブスクリプションプランを変更しました',
                        'message': '{first_name}{last_name}様Enclopediaファッションレンタルサービスをご利用頂きありがとうございます。\
                                    \n{plan}への変更が完了しました,次回更新日は{update_date}となります。\
                                    引き続きEnclopediaファッションレンタルサービスをよろしくお願いします。'.format(first_name=user.first_name, last_name=user.last_name, plan=customer.plan,  update_date=date)
                        }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    print('changed premiume plan to basic plan')
                    subscription_info = stripe.Subscription.list(
                    customer=customer.customer_id,
                    status='active'
                    )
                    subscription_update = stripe.Subscription.modify(
                    subscription_info['data'][0].id,
                    proration_behavior='none',
                    items=[
                        {
                            "price": price_id,
                        },
                    ],)

                    stripe.SubscriptionItem.delete(
                        subscription_info['data'][0]['items']['data'][0].id,
                        proration_behavior="none"
                        )
                    #元のitemを削除後にsubscriptionアップデートプランに加入する

                    customer.price_id = price_id
                    customer.plan = data['plan']
                    update_date = datetime.datetime.fromtimestamp(subscription_update.start_date)
                    customer.update_date = update_date
                    customer.save(update_fields=["plan", 'update_date'])
                    date = customer.update_date.strftime('%Y年%m月%d日')
                    data = {
                        'title': 'サブスクリプションプランを変更しました',
                        'message': '{first_name}{last_name}様Enclopediaファッションレンタルサービスをご利用頂きありがとうございます。\
                                    \n{plan}への変更が完了しました,次回更新日は{update_date}となります。\
                                    引き続きEnclopediaファッションレンタルサービスをよろしくお願いします。'.format(first_name=user.first_name, last_name=user.last_name, plan=customer.plan,  update_date=date)
                        }
                    return Response(data, status=status.HTTP_200_OK)
            except:
                data = {
                    'title': 'サブスクリプションの更新に失敗しました。',
                    'message': 'サブスクリプションの更新に失敗しました。'
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                'message':'サブスクリプションプランをご契約していません。'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            
    def delete(self, request):
        user = request.user
        stripe_account = StripeAccount.objects.get(user_id=user)
        status_list = [1,3,4]
        reservation = Reservation.objects.select_related('user','adress').filter(user_id=user, status__in=status_list)
        #reservationが空
        if reservation:
            data = {
                'title': 'サブスクリプションの解約に失敗しました。',
                'message': '現在予約中の商品がございます、商品をご返却後再度ご解約手続きを行って下さい。'
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            if stripe_account.customer_id:
                # reservationを獲得後に未返却またはレンタル中のものがあればerrorを飛ばす量にす
                subscription = stripe.Subscription.list(
                    customer=stripe_account.customer_id,
                    status='active'
                )
                cancel_date = datetime.datetime.fromtimestamp(subscription['data'][0]['current_period_end'])
                delete_subscription = stripe.Subscription.delete(
                    subscription['data'][0]['id'],
                    invoice_now=True,
                    prorate=False
                )
                #delete から得たobjectに問題があるので500errorが発生している。
                if delete_subscription['status'] == 'canceled':
                    stripe_account.cancel_date = cancel_date
                    stripe_account.plan_id = None
                    stripe_account.save(update_fields=["cancel_date"])

                    data = {
                        'title': 'サブスクリプションの解約が完了しました。',
                        'message': 'サブスクリプションの解約が完了しました、サブスクリプションに関しまして引き続き契約終了日までご利用いただけます。'
                    }
                    return Response(data, status=status.HTTP_200_OK)


            else:
                data = {
                    'title': 'サブスクリプションの解約が完了しました。',
                    'message': 'サブスクリプションの解約が完了しました、ベーシックプランに関しまして引き続き契約終了日までご利用いただけます。'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)


class StripeCheckoutView(APIView):
    """fucntion related to onetime payment"""
    # 現在userに貸仕出し中のアイテムがあれば返却後に貸出可能となる
    def post(self, request):
        data = request.data
        user = request.user
        address = data['address']
        email = data['email']
        cart = data['cart_id']
        payment_method = data['payment_method']
        plan = data['plan']
        total_price=data['total_price']
        shipping_price=data['shipping_price']
        reserved_end_date=data['reserved_end_date']

        status_list = [1,3,4]
        reservations = Reservation.objects.select_related(
            'user', 'adress').filter(status__in=status_list)

        # 一度にレンタルできる数巣を制限する必要がある
        cartitems = CartItem.objects.filter(cart_id=cart)
        subscription_user_info = StripeAccount.objects.select_related('user_id').get(user_id=user)

        # 状態確認を行うためにresevationをここで作成しておく
        if (subscription_user_info.plan == plan == 'rental'):
            create_reservation = Reservation.objects.create(
                user=user,
                adress_id=address,
                status=0,
                plan=plan,
                reserved_end_date=reserved_end_date,
                total_price=total_price,
                shipping_price=shipping_price
            )
            try:
                #値が０の場合に[0]は参照できないのでerrorが発生する
                if len(reservations) > 0:
                    raise
                else:
                # トランザクションで失敗すれば元に戻すようにする
                    with transaction.atomic():
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
                        if not subscription_user_info.customer_id:
                            customer = stripe.Customer.create(
                                email=email,
                                payment_method=payment_method,
                                invoice_settings={
                                    'default_payment_method': payment_method
                                }
                            )['id']

                            #setupIntentを通じて支払いがformなしてできるようになっている。
                        # customerが存在しなかった場合に作成する
                        else:
                            customer = subscription_user_info.customer_id
                            # paymentIntentに関して支払い完了後にstateで支払い状態を確認するコードを書く
                        response = stripe.PaymentIntent.create(
                            customer=customer,
                            payment_method_types=['card'],
                            payment_method=payment_method,
                            currency='jpy',
                            amount=(total_price + shipping_price),
                            confirm=True
                        )

                        # 支払いが成功した場合の処理
                        if response['status'] == 'succeeded':
                            # reservationitemの登録
                            for cartitem in cartitems:
                                reservation_item = ReservationItem.objects.create(
                                    reservation=create_reservation,
                                    product=cartitem.product,
                                    quantity=cartitem.quantite
                                )
                                if cartitem.variation.exists():
                                    reservation_item.variation.add(cartitem.variation)
                            #statusをacceptにする
                            create_reservation.status = 1
                            create_reservation.is_reserved = True
                            create_reservation.save(update_fields=["status", "is_reserved"])
                            # cartアイテムも同時に削除されるようにする
                            Cart.objects.get(user=user).delete()
                            data = {
                                'title': '予約完了',
                                'message':'予約が完了致しました、商品お届けまで３日ほど時間を頂いております（天候等の影響により到着が遅れる場合がございます、ご了承下さい。)発送完了後に商品発送後通知を致します、今しばらくお待ち下さい。'
                                }
                            return Response(data, status=status.HTTP_200_OK)
                        # 支払いが失敗した場合の処理
                        # 支払いに失敗したら例外を発生させなければならない
                        elif response.data['status'] == 'requires_payment_method':
                            create_reservation.status = 2
                            create_reservation.is_reserved = False
                            create_reservation.save(update_fields=["status", "is_reserved"])
                            for cartitem in cartitems:
                                ReservationItem.objects.create(
                                    reservation=create_reservation,
                                    product=cartitem.product,
                                    quantity=cartitem.quantite
                                )
                                if cartitem.variation.exists():
                                    reservation_item.variation.add(cartitem.variation)
                            message = {
                                'title' : '支払いに失敗しました。',
                                'message':'支払いが受付けられませんでした、カード情報を更新の上再度予約手続きをして下さい。'}
                            return Response(message, stauts=status.HTTP_400_BAD_REQUEST)

            except:
                # 支払いに失敗した場合には状態をdeniedにして保存する
                create_reservation.status = 2
                create_reservation.is_reserved = False
                create_reservation.save()
                for cartitem in cartitems:
                    ReservationItem.objects.create(
                        reservation=create_reservation,
                        product=cartitem.product,
                        quantity=cartitem.quantite
                    )
                    if cartitem.variation.exists():
                        reservation_item.variation.add(cartitem.variation)
                    # cartアイテムも同時に削除されるようにする
                message = {
                    'message':'予約に失敗しました、現在商品をレンタル中か在庫が切れている可能性があります。',
                    }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

class CreditInfoView(APIView):
    """edit credit cart infomation registered stripe"""
    def get(self, request):
        #paymentmethodidも返すようにする
        customer = StripeAccount.objects.get(user_id=request.user)
        if customer.customer_id:
            # クレジットカード情報を取得

            info = stripe.PaymentMethod.list(
                customer=customer.customer_id,
                type="card"
            ).data[0]

            if info:
                data = {
                    'payment_method_id':info.id,
                    'number': info.card.last4,
                    'brand': info.card.brand,
                    'exp_month': info.card.exp_month,
                    'exp_year': info.card.exp_year,
                }

                return Response(data, status=status.HTTP_200_OK)
            else:
                message = {'message':'クレジットカード情報が存在しません、登録を行なって下さい。'}
                return Response(message, stauts=status.HTTP_404_NOT_FOUND)
        else:
            message = {'message': 'クレジットカード情報の取得に失敗しました。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        data = request.data
        email = data['email']
        payment_method = request.data['payment_method']
        stripe_accout = StripeAccount.objects.get(user_id=request.user)
        #setUp Intentでカード情報を登録してもpaymnetMethod.attachでuserと結びつけを行う必要がある。
        try:
            #cusotomerが作成されていない状態ですると初期支払い方法が登録される
            customer_data = stripe.Customer.list(email=email)
            if len(customer_data) == 0:
                #userが登録を行なってない場合はdefault_settingsにpayment_methodを登録
                customer = stripe.Customer.create(
                    email=email,
                    payment_method=payment_method,
                    invoice_settings={
                        'default_payment_method': payment_method
                    },
                )

                stripe_accout.customer_id = customer.id
                stripe_accout.save()
                #customer_idのみを登録しておく
                credit_info = stripe.PaymentMethod.retrieve(payment_method)
                data = {
                    'payment_method_id':credit_info.id,
                    'number': credit_info.card.last4,
                    'brand': credit_info.card.brand,
                    'exp_month': credit_info.card.exp_month,
                    'exp_year': credit_info.card.exp_year,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                customer = StripeAccount.objects.get(user_id=request.user)
                set_up_intent = stripe.SetupIntent.list(customer=customer.customer_id)
                if len(set_up_intent) == 0:
                    stripe.SetupIntent.create(
                        customer=customer.customer_id,
                        payment_method=payment_method
                    )
                    message = {'message': 'クレジット情報を登録しました。'}
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    if set_up_intent.data[0].status == 'canceled':
                        stripe.SetupIntent.create(
                            customer=customer.customer_id,
                            payment_method=payment_method
                        )
                    else:
                        stripe.SetupIntent.modify(
                            set_up_intent.data[0].id,
                            payment_method_types=["card"],
                            payment_method=payment_method
                        )
                    stripe.PaymentMethod.attach(
                        payment_method,
                        customer=customer.customer_id
                    )
                    stripe.Customer.modify(
                        customer.customer_id,
                        invoice_settings ={
                            'default_payment_method': payment_method
                        }
                    )
                    message = {'message': 'クレジットカード情報を更新しました。'}
                    return Response(message, status=status.HTTP_200_OK)
        except:
            message = {'message': 'クレジットカード情報登録ができませんでした。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        data = request.data
        payment_mehtod= data['payment_method']
        try:
            customer = StripeAccount.objects.get(user_id=user)
            stripe.PaymentMethod.attach(
                payment_mehtod,
                customer=customer.customer_id
            )
            stripe.Customer.modify(
                customer.customer_id,
                invoice_settings ={
                    'default_payment_method':payment_mehtod
                }
            )
            message = {'message': 'クレジットカード情報の登録が完了しました。'}
            return Response(message, status=status.HTTP_200_OK)
        except:
            message = {'message':'クレジットカード情報変更に失敗しました。'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        payment_method = data['payment_method']

        try:
            customer_id = StripeAccount.objects.get(user=user).id
            stripe.PaymentMethod.detach(payment_method, customer=customer_id)
            return Response(message, status=status.HTTP_200_OK)
        except:
            message = 'クレジットカード情報の削除に失敗しました。'
            return Response(message, status.HTTP_400_BAD_REQUEST)

class StripeUserInfoView(generics.RetrieveDestroyAPIView):
    queryset = StripeAccount.objects.all()
    serializer_class = StripeSubscriptionSerializer

    def get(self, request):
        instance = get_object_or_404(self.queryset, user_id=request.user)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.request, user_id=request.user)
            stripe.Customer.delete(instance.customer_id)
            data = {'message': 'stripeアカウントの削除が完了しました'}
            return Response(data, status=status.HTTP_200_OK)
        except:
            data = {'message':'ストライプアカウントの削除に失敗しました'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class StripeSubscriptionInvoiceView(APIView):
    """subscriptionようのinvoiceの取得"""
    def get(self, request):
        try:
            customer_id = StripeAccount.objects.get(
                user_id=request.user
            ).customer_id
            if customer_id:
                subscription_id = stripe.Subscription.list(customer=customer_id)[0]
                invoice = stripe.Invoice.list(customer=customer_id, subscription=subscription_id).data
                return Response(invoice, status=status.HTTP_200_OK)
            else:
                message = {"message": "サブスクリプションに登録していません"}
                return Response(message, status=status.HTTP_404_NOT_FOUND)
        except:
            message = {"message": "サブスクリプションに関する請求情報が取得できませんでした"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class StripeUpcomingInvoice(APIView):
    """まだ作成されていないinvoiceについて確認するために必要"""
    def get(self, request):
        try:
            customer_id = StripeAccount.objects.get(
                user_id=request.user
            ).customer_id
            if customer_id:
                invoice = stripe.Invoice.upcoming(customer=customer_id)
                return Response(invoice, status = status.HTTP_200_OK)
            else:
                message = {"message": "サブスクリプションに登録していません"}
                return Response(message, status=status.HTTP_404_NOT_FOUND)
        except:
            message = {"message": "サブスクリプションに関する請求情報が取得できませんでした"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

#checkoutようのinvoiceを表示
class StripeInvoiceView(APIView):
    """function to related invoice of stripe"""
    def get(self, request):
        try:
            customer_id = StripeAccount.objects.get(
                user_id=request.user).customer_id
            if customer_id:
                #最初のキーが取り出されてしまうのでlistをreverseして最新のdataを取得する
                invoice = stripe.Invoice.list(customer=customer_id).data[0]
                end_date = datetime.datetime.fromtimestamp(
                    invoice.lines.data[0].period.end)
                start_date = datetime.datetime.fromtimestamp(
                    invoice.lines.data[0].period.start
                )
                created_date = datetime.datetime.fromtimestamp(
                    invoice.created
                )
                data = {
                    'amount': invoice.lines.data[0].amount,
                    'end_date': end_date,
                    'start_date': start_date,
                    'created_date': created_date,
                    'invoice_url': invoice.invoice_pdf
                }

                return Response(data, status=status.HTTP_200_OK)
        except:
            message = {'message': 'インボイスを取得できませんでした'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class SetupIntentView(APIView):
    
    def get(self, request):
        user = request.user
        customer = StripeAccount.objects.get(user_id=user)
        info = stripe.SetupIntent.list(customer=customer.customer_id)
        payment_method =stripe.PaymentMethod.retrieve(info['data'][0].payment_method)
        
        return Response(payment_method)
    
    def delete(self,request):
        user = request.user
        customer = StripeAccount.objects.get(user_id=user)
        info = stripe.SetupIntent.list(customer=customer.customer_id)
        stripe.SetupIntent.cancel(info.data[0].id)
        return Response('成功')
        
@csrf_exempt
def webhook_view(request):
    """function to related stripe webhook"""
    endpoint_secret = env("STRIPE_END_POING_SECRET")
    payload = request.body.decode('utf-8')
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    if event['type'] == 'checkout.session.async_payment_successed':
    #サブスクリプション更新支払い完了時時のイベントをトリガー
        checkout = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_failed':
    #サブスクリプション更新時支払い失敗のイベントをトリガー
        #サブスクリプションの支払い時のもみ応答するwebhook
        checkout = event['data']['object']
        stripe_account = StripeAccount.objects.get(customer_id=checkout.customer)
        stripe_account.is_active = False
        stripe_account.save()

    #subscriptionの数日前に発生する
    elif event['type'] == 'invoice.upcoming':
    #寒くリプション更新時の
        try:
            data = event['data']['object']
            stripe_account = StripeAccount.objects.get(customer_id=data.customer)
            tasks.subscription_update_confirmation_notification(stripe_account.user_id)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif event['type'] == 'invoice.payment_succeeded':
    #サブスクリプション更新日の支払いが完了時に通知
    #支払いが完了したことを伝えるメールと通知を送信し、update_dateを更新する
        data = event['data']['object']
        try:
            today = datetime.datetime.now()
            stripe_account = StripeAccount.objects.get(customer_id=data.customer)
            stripe_account.update_date = today
            stripe_account.save()
            #taskから更新完了メールの送信
            return Response(status=status.HTTP_200_OK)
        except:
            logging.debug('通知に失敗')
            return Response(status=status.HTTP_200_OK)
    elif event['type'] == 'invoice.payment_failed':
        #サブスクリプション更新の支払いが失敗すると更新される
        data = event['data']['object']
        stripe_account = StripeAccount.objects.get(customer_id=data.customer)
        stripe_account.is_active = False
        #支払いができなかったことを通知し一時的にサブスクリプションが利用できなくなることを通知する
        try:
            tasks.update_subscription_payment_fail_notification(stripe_account)
            stripe_account.is_active = False
            stripe_account.save()
            return Response(status=status.HTTP_200_OK)
        except:
            logging.debug('サブスクリプション登録情報更新に失敗')
            return Response(status=status.HTTP_200_OK)
    elif event['type'] == 'invoice.paid':
        #サブスクリプションの支払いが完了したことを通知する
        data = event['data']['object']
        stripe_account = StripeAccount.objects.get(customer_id=data.customer)
        try:
            tasks.subscription_update_paid_success(stripe_account)
            return Response(status=status.HTTP_200_OK)
        except:
            logging.debug('サブスクリプション更新の通知に失敗しました。')
            return Response(status=status.HTTP_200_OK)
        
    else:
        print('イベントのハンドリングに失敗しました {}'.format(event['type']))
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(success=True, status=status.HTTP_200_OK)