from django.contrib import admin
from .models import Furniture, Room, Cleaning_Material, Technology, Dean_Approval_Needed_Item

# Register your models here.
class Furniture_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity',
                    'item_photo']

class Rooms_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity',
                    'item_photo']

class Cleaning_Materials_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity',
                    'item_photo']

class Technology_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity',
                    'item_photo']

class Dean_Approval_Needed_Admin(admin.ModelAdmin):
    list_display = ['item_id',
                    'item_name',
                    'item_category',
                    'item_description',
                    'item_total_quantity',
                    'item_current_quantity',
                    'item_borrowed_quantity',
                    'item_photo']

admin.site.register(Furniture, Furniture_Admin)
admin.site.register(Room, Rooms_Admin)
admin.site.register(Cleaning_Material, Cleaning_Materials_Admin)
admin.site.register(Technology, Technology_Admin)
admin.site.register(Dean_Approval_Needed_Item, Dean_Approval_Needed_Admin)