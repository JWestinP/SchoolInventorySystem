from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Borrowed_Item(models.Model):
    item_id = models.IntegerField()
    item_name = models.CharField(max_length = 128)
    item_quantity = models.IntegerField()
    item_returned = models.BooleanField()
    item_date_borrowed = models.DateField()
    item_date_returned = models.DateField(blank = True)
    item_photo = models.ImageField(blank = True, upload_to='borrowed_item')
    item_borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)