from django.contrib import admin
from .models import Unreturned_Item

# Register your models here.
class Unreturned_Items_Admin(admin.ModelAdmin):
    list_display = ['item_borrowed', 
                    'item_days_not_returned',
                    ]
    
admin.site.register(Unreturned_Item, Unreturned_Items_Admin)