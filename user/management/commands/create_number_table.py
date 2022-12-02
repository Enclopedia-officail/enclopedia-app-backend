from django.core.management.base import BaseCommand
from user.models import RandomNumber

import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            #１から９９９９までを登録
            authentication_nums = []
            for num in range(9999):
                num += 1
                authentication_num = f'{num:04}'
                authentication_nums.append(RandomNumber(number=authentication_num))
            RandomNumber.objects.bulk_create(authentication_nums)
        except:
            logger.error('RandomNumberモデルの作成に失敗しました')
            pass


