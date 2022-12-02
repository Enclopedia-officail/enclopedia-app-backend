from django.core.management.base import BaseCommand
from reservation.models import Reservation
from datetime import datetime
import csv


class Command(BaseCommand):
    """compile csv files of users who have not returned product"""

    def get_reservation(self):
        today = datetime.now()
        end_day = today.replace(hour=0, minute=0, second=0)
        reservatoins = Reservation.objects.filter(status=1, reserved_end_date__lte=end_day)
        return reservatoins
    
    def handle(self):
        reservations = self.get_reservation()
        user_list = []
        for reservation in reservations:
            user = []
            user.append(reservation.user.email)
            user.append(reservation.user.first_name)
            user.append(reservation.last_name)
            user_list.append(user)

        today = datetime.now().strftime('%Y-%m-%d')
        header = ['email', 'first_name', 'last_name']

        with open(today + 'return_prodcut.csv' , 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(user_list)

        
            





