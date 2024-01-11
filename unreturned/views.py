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
    unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + unreturned_items.item_borrowed.item_quantity

    item = Stock.objects.get(pk = item_stock_id)
    item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
    item.save()

    unreturned_items.delete()

    # for checking
    print(unreturned_items.item_borrowed.item_stock.item_current_quantity)
    print(item)
    print(item.item_current_quantity)
    # for checking


    return redirect('unreturned')