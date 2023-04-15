from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from subscription.models import Coupon, InvitationCode, Issuing, Invitation
from user.models import Account
from datetime import datetime, timedelta, date
import random
import string


#DISTRIBUTE_COUPON_URL = reverse('subscription:distribute_coupon')
UTILISED_COUPON_URL = reverse('subscription:utilised_coupon')
DISCOUNT_PRICE_URL = reverse('subscription:discount_price')
INVITATION_COUPON_URL = reverse('subscription:invitation_coupon')

#Coupon modelテスト
class CouponModelTest(TestCase):
    def test_create_coupon_model(self):
        tomorrow = date.today() + timedelta(days=30)
        coupon = Coupon.objects.create(
            type = 'once',
            amount_off = 500,
            duration = 1,
            max_redemptions = 200,
            name = '500円割引クーポン',
            redeem_by = tomorrow
        )
        self.assertEqual(str(coupon), coupon.name)


#coupon配布の際の処理
"""
class DistributeCoupon(TestCase):

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
        tomorrow = datetime + timedelta(days=30)
        self.coupon = Coupon.objects.create(
            type = 'once',
            amount_off = 500,
            duration = 1,
            max_redemptions = 200,
            name = '500円割引クーポン',
            redeem_by = tomorrow
        )
    
    def test_distribute_coupon(self):
        
        data = {
            'coupon':  self.coupon.id
        }
        response = self.client.post(DISTRIBUTE_COUPON_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
"""

#couponを使用した際の処理
class UtilisedCouponTest(TestCase):
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
        tomorrow = date.today() + timedelta(days=30)
        self.coupon= Coupon.objects.create(
            type = 'once',
            amount_off = 500,
            duration = 1,
            max_redemptions = 200,
            name = '500円割引クーポン',
            redeem_by = tomorrow
        )

        Issuing.objects.create(
            user = self.user,
            coupon = self.coupon
        )
    
    def test_utilised_coupon(self):
        data = {
            'coupon': self.coupon.id
        }
        response = self.client.post(UTILISED_COUPON_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#couponeを適用させた際の価格を返すapi
class DiscountPriceTest(TestCase):
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
        tomorrow = date.today() + timedelta(days=30)
        self.coupon= Coupon.objects.create(
            type = 'once',
            amount_off = 500,
            duration = 1,
            max_redemptions = 200,
            name = '500円割引クーポン',
            redeem_by = tomorrow
        )
        
    
    def test_discount_test(self):
        #discountを反映した価格を返す
        data = {
            'coupon': self.coupon.id,
            'price': 5000
        }
        response = self.client.post(DISCOUNT_PRICE_URL, data)
        self.assertEqual(response.data['price'], 4500)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#友達を招待した際に両方にクーポンを発行するためのapi
class InvitationCopuonTest(TestCase):

    def generate_unique_string(self, length=6):
        result = ''.join(random.sample(string.ascii_letters, length))
        return result

    def setUp(self) -> None:
        self.client = APIClient()
        self.user_1 = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.user_2 = get_user_model().objects.create_user(
            first_name = 'test2',
            last_name = 'test2',
            username = 'test2',
            email = 'test2@example.com',
            phone_number = '08001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user_2)
        tomorrow = date.today() + timedelta(days=365)
        #使用期間を1年間とする
        self.coupon= Coupon.objects.create(
            type = 'once',
            amount_off = 1000,
            max_redemptions = 200,
            name = '友達招待クーポン',
            redeem_by = tomorrow
        )
        self.invitation = InvitationCode.objects.create(
            user = self.user_1,
            code = self.generate_unique_string(6)
        )   
    
    #初の招待でクーポンを発行
    def test_invitation_coupon(self):
        data = {
            'invitation_code': self.invitation.code,
            'phone_number': '08001610001'
        }
        response = self.client.post(INVITATION_COUPON_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #以前のアカウントでクーポンを受け取っている
    def test_received_coupon(self):
        Invitation.objects.create(
            InvitationCode = self.invitation,
            phone_number = '98001610001'
        )
        data = {
            'invitation_code': self.invitation.code,
            'phone_number': '98001610001'
        }
        response = self.client.post(INVITATION_COUPON_URL, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)