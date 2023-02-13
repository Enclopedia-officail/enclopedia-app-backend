from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from reservation.models import Reservation
from user.models import Adress
from product.models import Product

class ReservationGetTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
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
            status = 3,
            plan = 'basic',
        )


    def test_get_reservation(self):
        RESERVATION_GET_URL = ('/api/reservation/{}'.format(self.reservation))
        res = self.client.get(RESERVATION_GET_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 3)

class RservationGetFailedTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
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
        
    def test_get_reservation_failed(self):
        RESERVATION_GET_URL = ('/api/reservation/{}'.format(self.reservation))
        res = self.client.get(RESERVATION_GET_URL)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)