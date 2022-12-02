from django.conf import settings 
from django.core.management.base import BaseCommand

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

from analytics.models import Featured

from dateutil.relativedelta import relativedelta
import environ
import datetime
import os

import logging

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
            features = Featured.objects.all()
            if feature:
                features.delete()
            else:
                pass
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
                    if(list[1] == 'product'):
                        if int(res.metric_values[0].value) > previous_value:
                            product_list.append(res)
                        else:
                            product_list.insert(0, res)
                            previous_value = res.metric_values[0].value
                    else:
                        pass
            feature_list = []
            for i in range(100):
                list = product_list[i].dimension_values[0].value.split('/')
                product_id = list[-1]
                url = 'http://localhost:8000/api/' + str(product_list[i].dimension_values[0].value.split('/')[-1])
                view = product_list[i].metric_values[0].value
                feature = Featured(product_id=product_id, view=view, url=url)
                feature_list.append(feature)
            Featured.objects.bulk_create(feature_list)
        except:
            logger.error()