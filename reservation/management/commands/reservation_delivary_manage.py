from django.core.management.base import BaseCommand
from django.core import exceptions
from reservation.models import Reservation
import logging
import datetime
import pandas as pd

logger = logging.getLogger(__name__)

file_path = 'https://media.enclopedia-official.com/csv/reservation/list/'

class Command(BaseCommand):

    def get_reservations(self):
        today = datetime.datetime.now()
        date = today - datetime.timedelta(-1)
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=0, minute=0, second=0, microsecond=0)
        reservations = Reservation.objects.select_related('user', 'adress').prefetch_related('related_reservation_ite').filter(reserved_start_date__range=(start, end), status=1)
        reservation_info_list = []
        user_list = []
        for reservation in reservations:
            for item in reservation.related_reservation_item.all():
                reservation_info = []
                user_list.append(reservation.user.first_name + reservation.user.last_name)
                reservation_info.append(reservation.user.id)
                reservation_info.append(reservation.user.first_name + reservation.user.last_name)
                reservation_info.append(reservation.user.phone_number)
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
            header = ['顧客番号', '顧客名', '連絡先', '住所', '予約日時', 'プラン', '商品ID', '商品名']
            df = pd.DataFrame(reservation_info_list, columns=header, index=user_list)
            df.to_csv(file_path + filename + '.csv', mode='w', header=False)
            #csv fileを商品管理グループに送信
        except exceptions.BadRequest:
            logger.error('予約リストの書き出しに失敗しました')
    