from django.conf import settings
from django.core.management.base import BaseCommand
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from analytics.models import CartAddItem


import environ
import datetime
import os

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
    
    def handle(self, *args, **kwargs):
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
                dimensions=[Dimension(name='itemId'), Dimension(name='itemBrand'), Dimension(name='itemCategory')],
                metrics=[Metric(name=metrics)],
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
            )
            response = client.run_report(request)
            product_list = []
            previous_value = 0
            for data in [response]:
                list = data.rows
                for res in list:
                    print(res.dimension_values[2].value)
                    if res.dimension_values[1].value != "(not set)":
                        if int(res.metric_values[0].value) >  previous_value:
                            product_list.append(res)
                        else:
                            product_list.insert(0, res)
                            previous_value = res.metric_values[0].value
                    else:
                        pass
            cart_item_list = []
            print(product_list)
            for i in range(1):
                product_id = product_list[i].dimension_values[0].value
                brand = product_list[i].dimension_values[2].value
                view = product_list[i].metric_values[0].value
                cart_item = CartAddItem(product_id=product_id, brand_id=brand, view=view)
                cart_item_list.append(cart_item)
            CartAddItem.objects.bulk_create(cart_item_list)
            logger.debug()

