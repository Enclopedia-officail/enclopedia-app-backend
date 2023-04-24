from django.db import models
import uuid
from user.models import Account

"""
class Styling(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    silhouette = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    situation = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    material = models.CharField(max_length=100)

    def __str__(self):
        return self.id
"""
