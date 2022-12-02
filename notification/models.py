from user.models import Account
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# Create your models here.
#ポリモーフィックを利用して、一つのカラムに特定複数の外部キーを保存できるようにする
class Read(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, name='account')
    read = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Activitie(models.Model):
    class Meta:
        abstract = True
    read = GenericRelation(Read)

#館員全員に対して通知を行うようにする。
class News(Activitie):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

#ここのuserに対しての通知、商品返却など
#cronを使用して自動的に通知が行われるようにする
class Notification(Activitie):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

#userが通知を確認したかどうか判断するようにする
#

    
