from urllib.parse import urlencode
from django.urls import include, path, reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import URLPatternsTestCase, APIClient

from rest_framework import status

class ReservationListTest(TestCase, URLPatternsTestCase):
    """
    get data for a six-month period
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name='test',
            last_name='test',
            user_name='test',
            email='test@app.com',
            password='testpass'
        ),

        self.client.force_authenticate(self.user)

    urlpatterns = [
        path('api/reservation/', include('reservation.urls')),
    ]

    def test_get_rental_half_period_reservation_data(self):
        url = reverse('reservation:reservation_rental_half_year')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReservationGetWithUser(TestCase, URLPatternsTestCase):
    """
    confirm if reservation data exists for post product review'
    """
    
    def setUp(self):
        self.clent=APIClient()
        self.user = get_user_model().objects.create_user(
            first_name='test',
            last_name='test',
            user_name='test',
            email='test@app.com',
            password='testpass'
        )
