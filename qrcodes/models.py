from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/qrcodes')
    location = models.ImageField(upload_to='media/location', null=True)
    location_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name} - {self.description} is located at {self.location_name}'


class Warehouse_stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item.name} : {self.quantity}'

class QRScan(models.Model):
    scanned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    action = models.CharField(max_length=50)

    def formatted_scanned_at(self):
        # Преобразование времени в формат без миллисекунд и временной зоны
        return self.scanned_at.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"{self.scanned_by} has {self.action} {self.quantity} {self.item.name}(s) {self.formatted_scanned_at()}"