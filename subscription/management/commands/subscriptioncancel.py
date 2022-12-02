from django.core.management.base import BaseCommand
from subscription.models import StripeAccount
from datetime import datetime, timedelta
import pytz
import logging

logger = logging.getLogger(__name__)

#解約後に更新日になったuserを取得してサブスクリプションを無効化する
class Command(BaseCommand):
    """"""
    def get_subscription_account(self):
        print('hello')
        """deactivate plans for users whose subscriptions have been cancelled"""
        today = datetime.now(pytz.timezone('Asia/Tokyo'))
        end_day = today.replace(hour=0, minute=0, second=0)
        start_day = end_day - timedelta(days=1)
        try:
            #update_期間は削除した期間なので更新の期間ではない、start_dateから一ヶ月がサブスクリプションの終了期間となる
            accounts = StripeAccount.objects.filter(cancel_date__range=[start_day,  end_day])
            print(accounts)
            return accounts
        except:
            logger.debug('サブスクリプションを解約したユーザの削除に失敗しました 日付:{}'.format(today))
            pass

    def handle(self, *args, **options):
        """サブスクリプションを解約したアカウントを登録する"""
        try:
            accounts = self.get_subscription_account()
            account_list = []
            for account in accounts:
                account.is_active = False
                account.update_date = None
                account.cancel_date = None
                account.plan="rental"
                account.plan_id=None
                account_list.append(account)
            StripeAccount.objects.bulk_update(account_list, ['is_active', 'update_date', 'cancel_date', 'plan', 'plan_id'])
        except:
            logger.debug('サブスクリプションを解約したユーザを削除するのに失敗しました')
            pass