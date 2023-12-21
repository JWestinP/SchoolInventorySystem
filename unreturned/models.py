from django.db import models

# Create your models here.
class Unreturned_Item(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_quantity = models.IntegerField()
    item_date_borrowed = models.DateField()
    item_days_not_returned = models.IntegerField()
    item_photo = models.ImageField(blank = True)