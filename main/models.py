from django.contrib.auth.models import User
from django.db import models
from qrcodes.models import Warehouse_stock, QRScan

# Create your models here.

class News(models.Model):
    title = models.CharField('Title',max_length=100)
    content = models.TextField('Text',max_length=1000)
    date = models.DateField('Date',auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField('Image (Best: 800x600)',upload_to='news', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'



