from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from user.models import Adress
from reservation.models import Reservation,ReservationItem
from product.models import Product

class ReservationItemTest(TestCase):
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
        self.address = Adress.objects.select_related('user').create()
        self.product = Product.objects.create(
            product_name = 'test',
            is_subscription = 'basic',
        )
        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 4,
            plan = 'basic',
        )
        self.reservationItem = ReservationItem.objects.select_related('reservation','product').create(
            reservation = self.reservation,
            product = self.product,
        )

    def test_get_reservationItem(self):
        # ReservationItemをurlパラメータから取得するテスト
        res = self.client.get('/api/reservation/item/{}'.format(self.reservationItem.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_reservationItem_review(self):
        # ReservationItemのreviewを更新するテスト
        data = {'review': 5}
        res = self.client.patch('/api/reservation/item/{}'.format(self.reservationItem.id),data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['review'], 5)
