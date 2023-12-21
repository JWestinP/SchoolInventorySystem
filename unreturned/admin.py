from django.contrib import admin
from .models import Unreturned_Item

# Register your models here.
class Unreturned_Items_Admin(admin.ModelAdmin):
    list_display = ['item_id', 
                    'item_name', 
                    'item_quantity', 
                    'item_date_borrowed',
                    'item_days_not_returned',
                    'item_photo',
                    'item_borrower']
    
admin.site.register(Unreturned_Item, Unreturned_Items_Admin)