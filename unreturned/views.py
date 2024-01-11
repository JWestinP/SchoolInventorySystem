from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from recents.models import *
from home.models import *
from datetime import datetime

# Create your views here.
def unreturned(request):
    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

def admin_unreturned(request):
    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html',
                {'unreturned_items': unreturned_items})

def return_item(request, item_id, item_stock_id):
    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    return_quantity = unreturned_items.item_borrowed.item_quantity
    current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
    current_quantity = current_quantity + return_quantity

    # borrowed_items = Borrowed_Item.objects.get(item_stock_id)
    # borrowed_items  = borrowed_items + return_quantity

    # unreturned_items.delete()
    return redirect('unreturned')