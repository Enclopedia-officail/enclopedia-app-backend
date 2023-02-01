from django.test import TestCase
from django.test import Client
from django.test import reverse
from django.contrib.auth import get_user_model

#buying adminようにテストを記述するようにする
class BuyingAdminTest(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model()