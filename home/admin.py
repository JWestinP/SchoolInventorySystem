from django.contrib import admin
from .models import Furniture, Room, Cleaning_Material, Technology

# Register your models here.
class Furniture_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity']

class Rooms_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity']

class Cleaning_Materials_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity']

class Technology_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity']

admin.site.register(Furniture, Furniture_Admin)
admin.site.register(Room, Rooms_Admin)
admin.site.register(Cleaning_Material, Cleaning_Materials_Admin)
admin.site.register(Technology, Technology_Admin)
