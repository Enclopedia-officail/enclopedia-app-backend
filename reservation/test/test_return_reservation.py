from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.models import Adress
from reservation.models import Reservation


RESERVATION_LIST_URL = reverse('reservation:shipping_list')

class ShippingReservationsTest(TestCase):
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

        # statusが異なるデータを作成
        for _ in range(2):
            self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 4,
            plan = 'basic',
        )
        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 3,
            plan = 'basic',
        )

    def test_shipping_list(self):
        # 取得したリストが全てSHIPPINGかテスト
        res = self.client.get(RESERVATION_LIST_URL)
        print(res.data)
        statusNum = []
        for result in res.data['results']:
            statusNum.append(result['status'])
        print(RESERVATION_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(statusNum.count(4) == len(statusNum), True)

class CompleteReturnTest(TestCase):
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

        self.reservation = Reservation.objects.select_related('user', 'adress').create(
            user = self.user,
            adress = self.address,
            is_reserved = True,
            status = 4,
            plan = 'basic',
            return_date = None
        )

    def test_complete_retrun(self):
        # 返却完了処理実行後、fieldが更新されるかテスト
        res = self.client.patch('/api/reservation/complete_return/{}'.format(self.reservation.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 5)
        self.assertEqual(res.data['is_reserved'], False)
        self.assertEqual(res.data['return_date'] is not None , True)
