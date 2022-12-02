from django.core.management.base import BaseCommand
from django.core import exceptions
from reservation.models import Reservation
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
import pandas as pd

file_path = str(settings.BASE_DIR) +  '/csv/'

class Command(BaseCommand):
    """compile the previous day's reserved items into a csv file"""

    def get_reservation(self):
        today = datetime.now()
        start_day = (today - relativedelta(months=1)).replace(day=1, hour=0, minute=0,second=0)
        reservations = Reservation.objects.select_related('user', 'adress').prefetch_related('related_reservation_item').filter(reserved_start_date__range=(start_day,today), status__in=[1,3,4,5])
        reservation_info_list = []
        user_list = []
        for reservation in reservations:
            for item in reservation.related_reservation_item.all():
                reservation_info = []
                user_list.append(reservation.user.first_name + reservation.user.last_name)
                reservation_info.append(reservation.user.id)
                reservation_info.append(reservation.adress.prefecture + reservation.adress.region + reservation.adress.address + reservation.adress.building_name)
                reservation_info.append(reservation.reserved_start_date)
                reservation_info.append(reservation.plan)
                reservation_info.append(item.product.id)
                reservation_info.append(item.product.product_name)
                reservation_info_list.append(reservation_info)
        return reservation_info_list, user_list
    
    def handle(self, *args, **options):
        try:
            filename = datetime.now().strftime('$Y-$m-%d')
            reservation_info_list, user_list = self.get_reservation()
            header = ['顧客番号', '住所', '予約日時', 'プラン', '商品ID', '商品名']
            df = pd.DataFrame(reservation_info_list, columns=header, index=user_list)
            df.to_csv(file_path + filename + '.csv', mode='a', header=False)
        except exceptions.BadRequest:
            pass