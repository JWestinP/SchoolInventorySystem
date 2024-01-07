from django.db import models

# Create your models here.
class Category(models.Model):
    item_category = models.CharField(max_length = 64)

    def __str__(self):
        return self.item_category

class Item(models.Model):
    item_id = models.BigAutoField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_description = models.CharField(max_length = 256)
    item_photo = models.ImageField(blank = True, upload_to='item_photo')

    def __str__(self):
        return f"{self.item_id} - {self.item_name} ({self.item_category})"

class Stock(models.Model):
    item_information = models.OneToOneField(Item, on_delete=models.CASCADE)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item_information.item_id} - {self.item_information.item_name} ({self.item_information.item_category})"


