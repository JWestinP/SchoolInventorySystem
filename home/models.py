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
    item_photo = models.ImageField(blank = True, upload_to='furniture')
    
class Room(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()
    item_photo = models.ImageField(blank = True, upload_to='room')

class Cleaning_Material(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()
    item_photo = models.ImageField(blank = True, upload_to='cleaning_material')
        
class Technology(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()
    item_photo = models.ImageField(blank = True, upload_to='technology')    

class Dean_Approval_Needed_Item(models.Model):
    item_id = models.IntegerField(primary_key = True)
    item_name = models.CharField(max_length = 128)
    item_category = models.CharField(max_length = 128)
    item_description = models.CharField(max_length = 256)
    item_total_quantity = models.IntegerField()
    item_current_quantity = models.IntegerField()
    item_borrowed_quantity = models.IntegerField()    
    item_photo = models.ImageField(blank = True, upload_to='dean_item')