from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Unreturned_Item(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_quantity = models.IntegerField()
    item_date_borrowed = models.DateField()
    item_days_not_returned = models.IntegerField()
    item_photo = models.ImageField(blank = True, upload_to='borrowed_item')
    item_borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)