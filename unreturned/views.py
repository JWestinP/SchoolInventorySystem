from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from recents.models import *
from home.models import *
from datetime import datetime
from home.decorators import allowed_users
from home.decorators import allowed_users
from django.db.models import Q  # Import Q for complex queries

# Create your views here.
# test
@allowed_users(allowed_roles=['Faculty'])
def unreturned(request):
    user = request.user
    unreturned_items = Unreturned_Item.objects.filter(item_borrowed__item_borrower = user)


    # unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

@allowed_users(allowed_roles=['Admin'])
def admin_unreturned(request):
    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html',
                {'unreturned_items': unreturned_items})

def return_item(request, item_id, item_stock_id):

    # determine what item from ureturned, and compute the quantity when returning item
    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + unreturned_items.item_borrowed.item_quantity

    # get the item using stock id, update the item quantity and save it to database
    item = Stock.objects.get(pk = item_stock_id)
    item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
    item.save()

    # delete the item from unreturned
    unreturned_items.delete()

    # for checking
    # print(unreturned_items.item_borrowed.item_stock.item_current_quantity)
    # print(item)
    # print(item.item_current_quantity)
    # for checking

    # redirect again the user to the page of "unreturned" after the process
    return redirect('unreturned')

def admin_return_item(request, item_id, item_stock_id):
    # determine what item from ureturned, and compute the quantity when returning item
    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + unreturned_items.item_borrowed.item_quantity

    # get the item using stock id, update the item quantity and save it to database
    item = Stock.objects.get(pk = item_stock_id)
    item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
    item.save()

    # delete the item from unreturned
    unreturned_items.delete()

    # for checking
    # print(unreturned_items.item_borrowed.item_stock.item_current_quantity)
    # print(item)
    # print(item.item_current_quantity)
    # for checking

    # redirect again the user to the page of "unreturned" after the process
    return redirect('admin_unreturned')

@allowed_users(allowed_roles=['Admin'])
def admin_search_unreturned(request):
    query = request.GET.get('q', '')

    if query:
        # Adjust this query based on your model relationships
        items = Unreturned_Item.objects.filter(
            Q(item_borrowed__item_stock__item_information__item_name__icontains=query) |
            Q(item_borrowed__item_borrower__username__icontains=query)
        )
    else:
        items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html', {'unreturned_items': items, 'query': query})


@allowed_users(allowed_roles=['Faculty'])
def faculty_search_unreturned(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        # Adjust this query based on your model relationships
        items = Unreturned_Item.objects.filter(
            Q(item_borrowed__item_stock__item_information__item_name__icontains=query) |
            Q(item_borrowed__item_borrower__username__icontains=query)
        )
    else:
        items = Unreturned_Item.objects.filter(item_borrowed__item_borrower=user)

    return render(request, 'unreturned/unreturned.html', {'unreturned_items': items, 'query': query})