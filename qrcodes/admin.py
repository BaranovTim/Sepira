from django.contrib import admin

from . import models

admin.site.register(models.Item)
admin.site.register(models.QRScan)
admin.site.register(models.Warehouse_stock)

