from django.db import models

# Create your models here.
class Furniture(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()
    
class Room(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()

class Cleaning_Material(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()

class Technology(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()    

class Dean_Approval_Needed_Item(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()    