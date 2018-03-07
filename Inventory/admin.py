from django.contrib import admin

# Register your models here.
from Inventory.models import Inventory, InventoryItems

admin.site.register(Inventory)
admin.site.register(InventoryItems)