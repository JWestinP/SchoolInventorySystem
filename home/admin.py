from django.contrib import admin
from .models import *

# Register your models here.
class Category_Admin(admin.ModelAdmin):
    list_display = ['item_category']
    
class Item_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_photo']

class Stock_Admin(admin.ModelAdmin):
    list_display = ['item_information',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity']
    
admin.site.register(Category, Category_Admin)
admin.site.register(Item, Item_Admin)
admin.site.register(Stock, Stock_Admin)