from urllib.parse import urlencode
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

class ProductTagPriceTest(APITestCase, URLPatternsTestCase):
    """
        get product for each tag
    """
    urlpatterns = [
        path('api/product/', include('product.urls')),
    ]
    
    def test_product_tag_price(self):
        url = "".join([reverse('product:tag_price_order'),'?', urlencode(dict(tag=2))])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_product_tag_price_desc(self):
        url = "".join([reverse('product:tag_price_order'), '?', urlencode(dict(tag="1"))])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)