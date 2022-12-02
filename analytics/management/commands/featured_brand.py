from django.conf import settings
from django.core.management.base import BaseCommand
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

from category.models import Brand
from analytics.models import FeaturedBrand

import environ
import datetime
import os
import re

import logging


logger = logging.getLogger(__name__)

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))
logger = logging.getLogger(__name__)

class Command(BaseCommand):
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

    def handle(self, *args, **options):
        try:
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
            product_list = []
            previous_value = 0
            for data in [response]:
                list = data.rows
                for res in list:
                    number = res.dimension_values[0].value
                    if(re.fullmatch('\d+', number)):
                        if int(res.metric_values[0].value) > previous_value:
                            product_list.append(res)
                        else:
                            product_list.insert(0, res)
                            previous_value = res.metric_values[0].value
                    else:
                        pass
            feature_list = []
            #dataを取得したい分がlist内にない場合rangeで回した処理
            for i in range(4):
                number = product_list[i].dimension_values[0].value
                brand = Brand.objects.get(id=number)
                url = 'http://localhost:8000/api/' + brand.brand_name + '?number=' + str(brand.id)
                view = product_list[i].metric_values[0].value
                feature_brand = FeaturedBrand(brand=brand, url=url, view=view)
                feature_list.append(feature_brand)
            FeaturedBrand.objects.bulk_create(feature_list)
        except:
            logger.error('')

