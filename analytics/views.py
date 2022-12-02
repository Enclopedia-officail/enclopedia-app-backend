from django.conf import settings
from yaml import serialize
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_list_or_404

from .models import Featured, FeaturedBrand, CartAddItem
from .serializers import FaturedSerializer, FeatureBrandSerializer, CartAddItemSerializesr

import datetime
from dateutil.relativedelta import relativedelta
import environ
import logging
import os
import re
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

logger = logging.getLogger(__name__)

class FeatureListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Featured.objects.select_related('product').order_by('-view').all()
    serializer_class = FaturedSerializer

    def get(self, request):
        features = get_list_or_404(self.queryset)
        serializer = self.serializer_class(features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeatureBrandListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = FeaturedBrand.objects.select_related('brand').order_by('-view').all()
    serializer_class = FeatureBrandSerializer

    def get(self, request):
        featured_brands = get_list_or_404(self.queryset)
        serializer = self.serializer_class(featured_brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartAddProductInfoView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = CartAddItem.objects.select_related('product', 'brand').order_by('-view').all()
    serializer_class = CartAddItemSerializesr

    def get(self, request):
        response = get_list_or_404(self.queryset)
        serializser = self.serializer_class(response, many=True)
        return Response(serializser.data, status=status.HTTP_200_OK)

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = str(settings.BASE_DIR) + '/analytics/client-secret.json'
VIEW_ID = "266049021"
today = datetime.datetime.today()
month = today - relativedelta(month=1)

""

class GooglaAnalyticsView(APIView):
    permission_classes = (AllowAny,)
    #gogle apiのテスト
    def get(self, request):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPE)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        #発行したk流アイアント側に問題があり接続ができない状態になってリウ。
        response = analytics.reports().batchGet(
            body={
            'reportRequests':[{
            'viewId': VIEW_ID,
            'pageSize': 10,
            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
            'metrics': [{'expression':'ga:pageviews'}],
            'dimensions':[{"name":"ga:pageTitle"},{"name":"ga:pagePath"}]
            }]}
        ).execute()
        return Response(response)
        

"""Google GA4 API"""
class GoogleAnalyticsGA4(APIView):
    permission_classes = (AllowAny,)
    def get_google_report_date(self, start_date, end_date, dimentsion, metrics):
        property_id = env("PROPERTY_ID")
        client = BetaAnalyticsDataClient()
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dimentsion)],
            metrics=[Metric(name=metrics)],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
        )
        response = client.run_report(request)
        return response
    
    def get_product(self, request):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(settings.BASE_DIR) + '/analytics/client_secret.json'
        today = datetime.datetime.today()
        end_date = today.strftime("%Y-%m-%d")
        td = datetime.timedelta(days=7)
        date = today - td
        start_date = date.strftime("%Y-%m-%d")
        dimension = 'pagePath'
        metrics = 'screenPageViews'
        #page viewについて取得
        response = self.get_google_report_date(start_date, end_date, dimension, metrics)
        product_list = []
        previous_value = 0
        for data in [response]:
            list = data.rows
            for res in list:
                list = res.dimension_values[0].value.split('/')
                print(list[-1])
                if(list[1] == 'product'):
                    if int(res.metric_values[0].value) > previous_value:
                        product_list.append(res)
                    else:
                        product_list.insert(0, res)
                        previous_value = res.metric_values[0].value
                else:
                    pass
        for i in range(10):
            print(product_list[i])
        return Response(response, status=status.HTTP_200_OK)

    def get_ecommerce_item(self):
        today = datetime.datetime.today()
        end_date = today.strftime("%Y-%m-%de")
        td = datetime.timedelta(day=7)
        date = today - td
        start_date = date.strftime("%Y-%m-%d")
        dimension = 'itemId'
        metrics = 'itemViews'
        #itemの閲覧数を取得
        response = self.get_google_report_date(start_date, end_date, dimension, metrics)
        return Response(response, status=status.HTTP_200_OK)

    def get_vkew(self, request):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(settings.BASE_DIR) + '/analytics/client_secret.json'
        today = datetime.datetime.today()
        end_date = today.strftime("%Y-%m-%d")
        td = datetime.timedelta(days=7)
        date = today - td
        start_date = date.strftime("%Y-%m-%d")
        dimensions = 'itemBrand'
        metrics = 'itemViews'
        #ブランドの閲覧数
        response = self.get_google_report_date(start_date, end_date, dimensions, metrics)
        print(response)
        return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(settings.BASE_DIR) + '/analytics/client_secret.json'
        property_id = env("PROPERTY_ID")
        today = datetime.datetime.today()
        end_date = today.strftime("%Y-%m-%d")
        td = datetime.timedelta(days=7)
        date = today - td
        start_date = date.strftime("%Y-%m-%d")
        metrics = 'addToCarts'
        client = BetaAnalyticsDataClient()
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name='itemId'), Dimension(name='itemBrand'), 
            Dimension(name='itemCategory'), Dimension(name="city"), Dimension(name='region'),
            Dimension(name='userAgeBracket'), Dimension(name='userGender')],
            metrics=[Metric(name=metrics), Metric(name='screenPageViews')],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
        )
        response = client.run_report(request)
        return Response(response, status.HTTP_200_OK)