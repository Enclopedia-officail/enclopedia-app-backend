from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from product.models import Product
from user.models import Adress
from reservation.models import Reservation, ReservationItem
from .. import models
from unittest.mock import patch, MagicMock
import environ

#api url

env = environ.Env()

CREATE_PAYMNET_URL = reverse('buying:payment')
CREATE_ORDER_URL = reverse('buying:order')
ORDER_ITEM_LIST_URL = reverse('buying:order_item_list')
BUYING_URL = reverse('buying:buying')
CREATE_ORDER_ITEM_URL = reverse('buying:order_item')

class OrderItemCreate(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.address = Adress.objects.get(user=self.user)
        self.payment = models.Payment.objects.create(
            user = self.user,
            payment_method='card',
            payment_id = 'fdsa08ca7st',
        )
        self.order = models.Order.objects.create(
            user = self.user,
            payment = self.payment,
            order_id = 'payment',
            total_price = 1000,
            tax = 0.1,
            status = 'Accepted',
            ip = '127.0.0.7'
        )

        self.product = Product.objects.select_related('category', 'brand', 'price').create(
            product_name = 'sample',
            description = 'sample',
            rating = 5.0,
            review_count = 1,
            stock = 1,
            img = 'https://test.com',
            is_available = True,
            is_subscription = 'rental',
        )

        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 3,
            plan = 'basic',
            ip = '127.0.0.1',
            payment_method = 'card',
            total_price = 1000,
            shipping_price = 800,
            shipping_number = '1201734'
        )

        self.reservation_item = ReservationItem.objects.select_related('product', 'reservation').create(
            reservation = self.reservation,
            product = self.product,
            quantity = 1,
        )

    def test_order_item_create(self):
        data = {
            "order_id":self.order.id,
            "reservation_item_id": self.reservation_item.id,
        }
        res = self.client.post(CREATE_ORDER_ITEM_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['is_ordered'], True)

class OrderItemListTest(TestCase):
    #orderItemテーブルをリストで取得するためのテスト
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.address = Adress.objects.get(user=self.user)
        self.payment = models.Payment.objects.create(
            user = self.user,
            payment_method='card',
            payment_id = 'fdsa08ca7st',
        )
        self.order = models.Order.objects.create(
            user = self.user,
            payment = self.payment,
            order_id = 'payment',
            total_price = 1000,
            tax = 0.1,
            status = 'Accepted',
            ip = '127.0.0.7'
        )

        self.product = Product.objects.select_related('category', 'brand', 'price').create(
            product_name = 'sample',
            description = 'sample',
            rating = 5.0,
            review_count = 1,
            stock = 1,
            img = 'https://test.com',
            is_available = True,
            is_subscription = 'rental',
        )

        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 3,
            plan = 'basic',
            ip = '127.0.0.1',
            payment_method = 'card',
            total_price = 1000,
            shipping_price = 800,
            shipping_number = '1201734'
        )

        self.reservation_item = ReservationItem.objects.select_related('product', 'reservation').create(
            reservation = self.reservation,
            product = self.product,
            quantity = 1,
        )

        models.OrderItem.objects.select_related('user', 'order', 'reservation_item').create(
            user=self.user,
            order = self.order,
            reservation_item = self.reservation_item,
            is_ordered = True,
        )
    
    def test_order_item_list(self):
        res = self.client.get(ORDER_ITEM_LIST_URL, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['is_ordered'], True)


class OrderItemGetTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.address = Adress.objects.get(user=self.user)
        self.payment = models.Payment.objects.create(
            user = self.user,
            payment_method='card',
            payment_id = 'fdsa08ca7st',
        )
        self.order = models.Order.objects.create(
            user = self.user,
            payment = self.payment,
            order_id = 'payment',
            total_price = 1000,
            tax = 0.1,
            status = 'Accepted',
            ip = '127.0.0.7'
        )

        self.product = Product.objects.select_related('category', 'brand', 'price').create(
            product_name = 'sample',
            description = 'sample',
            rating = 5.0,
            review_count = 1,
            stock = 1,
            img = 'https://test.com',
            is_available = True,
            is_subscription = 'rental',
        )

        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 3,
            plan = 'basic',
            ip = '127.0.0.1',
            payment_method = 'card',
            total_price = 1000,
            shipping_price = 800,
            shipping_number = '1201734'
        )

        self.reservation_item = ReservationItem.objects.select_related('product', 'reservation').create(
            reservation = self.reservation,
            product = self.product,
            quantity = 1,
        )

        self.order_item =  models.OrderItem.objects.select_related('user', 'order', 'reservation_item').create(
            user=self.user,
            order = self.order,
            reservation_item = self.reservation_item,
            is_ordered = True,
        )
    
    def test_order_item_get(self):
        ORDER_ITEM_GET_URL = '/api/buying/order_item/{}'.format(self.order_item.id)
        res = self.client.get(ORDER_ITEM_GET_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class CreatePaymentTest(TestCase):
    #payment modelが使用できるかのテスト
    def create_payment(self):
        user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )

        payment = models.Payment.objects.create(
            user = user,
            payment_method='card',
            payment_id = 'fdsa08ca7st',
        )

        self.assertEqual(self.payment, payment.payment_id)

class PaymentCreateAPITest(TestCase):
    #payment model テーブルを作成するためのapiテスト
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)
    
    def test_create_payment(self):
        data = {
            'payment_method' : 'card',
            'payment_id' : 'fdsa08ca7st',
        }

        res = self.client.post(CREATE_PAYMNET_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

class OrderCreateAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.payment = models.Payment.objects.select_related('user').create(
            user = self.user,
            payment_method = 'card',
            payment_id = 'fdsa08ca7st',
        )
        self.client.force_authenticate(self.user)

    def test_create_order(self):
        data = {
            'payment': self.payment.id,
            'total_price': 1000,
            'tax': 0.1,
        }
        res = self.client.post(CREATE_ORDER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

class BuyingPaymentSuccessTest(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.payment = models.Payment.objects.create(
            user = self.user,
            payment_method='card',
            payment_id = 'fdsa08ca7st',
        )
        self.order = models.Order.objects.create(
            user = self.user,
            payment = self.payment,
            order_id = 'payment',
            total_price = 1000,
            tax = 0.1,
            status = 'Accepted',
            ip = '127.0.0.7'
        )
    #responseオブジェクトを指定する
    @patch('buying.views.BuyingReservationItemView.payment', MagicMock(return_value={'status': 'succeeded', 'id': 'sdaicd'}))
    def test_buying(self):
        data = {
            'order_id': self.order.id
        }
        res = self.client.post(BUYING_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['message'], '商品の購入が完了しました')

class BuyingPaymentFailedTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)        
        self.payment = models.Payment.objects.create(
            user = self.user,
            payment_method='card',
            payment_id = 'fdsa08ca7st',
        )
        self.order = models.Order.objects.create(
            user = self.user,
            payment = self.payment,
            order_id = 'payment',
            total_price = 1000,
            tax = 0.1,
            status = 'Accepted',
            ip = '127.0.0.7'
        )
    #mock return value部分にはresponseオブジェクトを指定する
    @patch('buying.views.BuyingReservationItemView.payment', MagicMock(return_value={'status': 'requires_payment_method', 'id': 'sdaicd'}))
    def test_payment_failed(self):
        data = {
            'order_id': self.order.id
        }
        res = self.client.post(BUYING_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'], '支払いに失敗しました。')