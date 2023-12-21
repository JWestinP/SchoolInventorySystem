from django.db import models

# Create your models here.
class Borrowed_Item(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_quantity = models.IntegerField()
    item_returned = models.BooleanField()
    item_date_borrowed = models.DateField()
    item_date_returned = models.DateField(blank = True)
    item_photo = models.ImageField(blank = True)
    item_borrower = models.CharField(max_length = 128, blank = True)