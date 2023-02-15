from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from notification.models import Todo
from reservation.models import Reservation, ReservationItem
from user.models import Adress
from product.models import Product


class TodoReturnItemCompletedTest(TestCase):
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
        self.address = Adress.objects.select_related('user').create()
        self.product = Product.objects.create(
            product_name = 'test',
            is_subscription = 'basic',
        )
        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 3,
            plan = 'basic',
        )
        self.client.force_authenticate(self.user)
        self.reservation_type = ContentType.objects.get(app_label='reservation', model='reservation')
        Todo.objects.create(
            user=self.user,
            title='test',
            thumbnail='http://test.com',
            url='http://test.com',
            content_type=self.reservation_type,
            object_id=self.reservation.id,
        )
        self.reservation_item_type = ContentType.objects.get(app_label='reservation', model='reservationitem')
        Todo.objects.create(
            user=self.user,
            title='test',
            thumbnail='http://test.com',
            url='http://test.com',
            content_type=self.reservation_item_type,
            object_id=self.reservation.id,
        )

    def test_todo_return_item_completed(self):
        TODO_ITEM_RETURM_URL = '/api/notification/todo/item/return'
        data = {'todo': True}
        res = self.client.put(TODO_ITEM_RETURM_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class TodoPurchasedItemTest(TestCase):
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
        self.address = Adress.objects.select_related('user').create()
        self.product = Product.objects.create(
            product_name = 'test',
            is_subscription = 'basic',
        )
        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 3,
            plan = 'basic',
        )
        self.reservationitem = ReservationItem.objects.select_related('reservation','product').create(
            reservation = self.reservation,
            product = self.product,
        )
        self.client.force_authenticate(self.user)
        self.todo_type = ContentType.objects.get(app_label='reservation', model='reservationitem')
        Todo.objects.create(
            user=self.user,
            title='test',
            thumbnail='http://test.com',
            url='http://test.com',
            content_type=self.todo_type,
            object_id=self.reservationitem.id,
        )

    def test_purchased_item(self):
        TODO_ITEM_PURCHASED_URL = '/api/notification/todo/item/purchased/{}'.format(self.reservationitem.id)
        data = {'todo': True, 'reservation_item_id': self.reservationitem.id}
        res = self.client.put(TODO_ITEM_PURCHASED_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
