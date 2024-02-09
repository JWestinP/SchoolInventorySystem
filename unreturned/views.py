from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from recents.models import *
from home.models import *
from datetime import datetime
from home.decorators import allowed_users
from home.decorators import allowed_users

# Create your views here.

@allowed_users(allowed_roles=['Faculty'])
def unreturned(request):
    user = request.user
    unreturned_items = Unreturned_Item.objects.filter(item_borrowed__item_borrower = user)

    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

@allowed_users(allowed_roles=['Admin'])
def admin_unreturned(request):
    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html',
                {'unreturned_items': unreturned_items})

def return_item(request, item_id, item_stock_id, borrow_form_id):

    pristine_no = request.POST.get("pristine")
    damaged_no = request.POST.get("damaged")

    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + unreturned_items.item_borrowed.item_quantity

    borrowed_item = Borrowed_Item.objects.get(pk=borrow_form_id)
    borrowed_item.item_returned = True
    borrowed_item.save()

    item = Stock.objects.get(pk = item_stock_id)
    item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
    item.save()

    unreturned_items.delete()

    return redirect('unreturned')

def admin_return_item(request, item_id, item_stock_id, borrow_form_id):

    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + unreturned_items.item_borrowed.item_quantity

    borrowed_item = Borrowed_Item.objects.get(pk=borrow_form_id)
    borrowed_item.item_returned = True
    borrowed_item.save()

    item = Stock.objects.get(pk = item_stock_id)
    item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
    item.save()

    unreturned_items.delete()

    return redirect('admin_unreturned')