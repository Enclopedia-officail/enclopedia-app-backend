from django.db import models
import uuid
from user.models import Account
from django.utils import timezone

def upload_img(instance, filename):
    image_filename = str(instance.id) + 'png'
    return "chatgpt/" + image_filename


class Styling(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    size = models.CharField(max_length=30)
    silhouette = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    situation = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    tops_fit = models.CharField(max_length=100)
    bottoms_fit = models.CharField(max_length=100)
    bottoms_length = models.CharField(max_length=100)
    image = models.FileField(upload_to=upload_img, default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)
