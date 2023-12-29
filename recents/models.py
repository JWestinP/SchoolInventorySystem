from django.db import models
from django.contrib.auth.models import User
from home.models import *

# Create your models here.
class Borrowed_Item(models.Model):
    borrow_form_id = models.BigAutoField(primary_key = True, blank=True)
    item_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    item_quantity = models.IntegerField()
    item_returned = models.BooleanField()
    item_date_borrowed = models.DateField()
    item_date_returned = models.DateField(blank = True)
    item_borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Borrow ID:{self.borrow_form_id} - {self.item_stock.item_information.item_name} ({self.item_quantity})"
    
