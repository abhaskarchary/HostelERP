from __future__ import unicode_literals
from django.db import models
import datetime


def item_id():
    last_id = InventoryItems.objects.all().order_by('item_id').last()
    if not last_id:
        return 'ITEM' + str(datetime.date.today().year) + '01'
    if str(datetime.date.today().year) !=last_id.item_id[4:8]:
        return 'ITEM' + str(datetime.date.today().year) + '01'
    item_id = last_id.item_id
    item_int = int(item_id[8:10])
    new_item_int = item_int + 1
    new_item_id = 'ITEM' + str(datetime.date.today().year) + str(new_item_int).zfill(2)
    return new_item_id


class InventoryItems(models.Model):
    item_id = models.CharField(max_length=10 ,default=item_id, primary_key=True)
    name = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=6,null=True)
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.item_id


def inventory_id():
    last_id = Inventory.objects.all().order_by('inv_log_id').last()
    if not last_id:
        return 'INV' + str(datetime.date.today().year) + '001'
    if str(datetime.date.today().year) !=last_id.inv_log_id[3:7]:
        return 'INV' + str(datetime.date.today().year) + '001'
    item_id = last_id.inv_log_id
    item_int = int(item_id[7:10])
    new_item_int = item_int + 1
    new_item_id = 'INV' + str(datetime.date.today().year) + str(new_item_int).zfill(3)
    return new_item_id


class Inventory(models.Model):
    inv_log_id = models.CharField(max_length=10,default=inventory_id , primary_key=True)
    date = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(InventoryItems)
    quantity = models.CharField(max_length=4)
    unit = models.CharField(max_length=6)
    price = models.CharField(max_length=5)
    description = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=9)

    def __str__(self):
        return self.inv_log_id




