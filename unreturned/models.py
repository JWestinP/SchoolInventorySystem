from django.db import models
from recents.models import Borrowed_Item

# Create your models here.
class Unreturned_Item(models.Model):
    item_borrowed = models.OneToOneField(Borrowed_Item, on_delete=models.CASCADE, null=True, blank=True)
    item_days_not_returned = models.IntegerField()
    