from django.contrib import admin
from .models import Borrowed_Item

# Register your models here.
class Borrowed_Items_Admin(admin.ModelAdmin):
    list_display = ['item_id', 
                    'item_name', 
                    'item_quantity', 
                    'item_returned', 
                    'item_date_borrowed',
                    'item_date_returned',
                    'item_photo']
    
admin.site.register(Borrowed_Item, Borrowed_Items_Admin)
