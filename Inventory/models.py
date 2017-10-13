from django.db import models
import datetime


# Create your models here.
#units n 3 categories

class Inventory(models.Model):
    inv_log_id = models.CharField(max_length=10, primary_key=True)
    date = models.DateTimeField()
    #category = models.CharField()
    #item_name = models.CharField()
    quantity = models.CharField(max_length=4)
    price = models.CharField(max_length=5)
    description = models.CharField(max_length=30, blank=True)
