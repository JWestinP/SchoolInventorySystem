from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from recents.models import *
from home.models import *
from datetime import datetime
from home.decorators import allowed_users
from home.decorators import allowed_users
from django.http import JsonResponse

# Create your views here.

#For initializing faculty unreturned
@allowed_users(allowed_roles=['Faculty'])
def unreturned(request):
    user = request.user
    unreturned_items = Unreturned_Item.objects.filter(item_borrowed__item_borrower = user)

    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

#For initializing admin unreturned
@allowed_users(allowed_roles=['Admin'])
def admin_unreturned(request):
    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html',
                {'unreturned_items': unreturned_items})

#For faculty returning item
def return_item(request, item_id, item_stock_id, borrow_form_id):
    pristine_no = request.POST.get("pristine")
    damaged_no = request.POST.get("damaged")

    total_no = int(pristine_no) + int(damaged_no)
    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    borrowed_item = Borrowed_Item.objects.get(pk=borrow_form_id)
    borrowed_item.item_returned = True
    borrowed_item.save()
    if total_no == borrowed_item.item_quantity:
        unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + int(pristine_no)
        unreturned_items.item_borrowed.item_stock.item_pristine_quantity = unreturned_items.item_borrowed.item_stock.item_pristine_quantity + int(pristine_no)
        unreturned_items.item_borrowed.item_stock.item_damaged_quantity = unreturned_items.item_borrowed.item_stock.item_damaged_quantity + int(damaged_no)
        unreturned_items.item_borrowed.item_stock.item_borrowed_quantity = unreturned_items.item_borrowed.item_stock.item_borrowed_quantity - borrowed_item.item_quantity

        unreturned_items.save()

        

        item = Stock.objects.get(pk = item_stock_id)
        item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
        item.item_pristine_quantity = unreturned_items.item_borrowed.item_stock.item_pristine_quantity
        item.item_damaged_quantity = unreturned_items.item_borrowed.item_stock.item_damaged_quantity
        item.item_borrowed_quantity = unreturned_items.item_borrowed.item_stock.item_borrowed_quantity
        item.save()

        unreturned_items.delete()
        return JsonResponse({'success': True})
    
    else:
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

#For admin returning item
def admin_return_item(request, item_id, item_stock_id, borrow_form_id):

    pristine_no = request.POST.get("pristine")
    damaged_no = request.POST.get("damaged")

    total_no = int(pristine_no) + int(damaged_no)
    unreturned_items = Unreturned_Item.objects.get(pk=item_id)
    borrowed_item = Borrowed_Item.objects.get(pk=borrow_form_id)
    borrowed_item.item_returned = True
    borrowed_item.save()
    if total_no == borrowed_item.item_quantity:
        unreturned_items.item_borrowed.item_stock.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity + int(pristine_no)
        unreturned_items.item_borrowed.item_stock.item_pristine_quantity = unreturned_items.item_borrowed.item_stock.item_pristine_quantity + int(pristine_no)
        unreturned_items.item_borrowed.item_stock.item_damaged_quantity = unreturned_items.item_borrowed.item_stock.item_damaged_quantity + int(damaged_no)
        unreturned_items.item_borrowed.item_stock.item_borrowed_quantity = unreturned_items.item_borrowed.item_stock.item_borrowed_quantity - borrowed_item.item_quantity

        unreturned_items.save()


        item = Stock.objects.get(pk = item_stock_id)
        item.item_current_quantity = unreturned_items.item_borrowed.item_stock.item_current_quantity
        item.item_pristine_quantity = unreturned_items.item_borrowed.item_stock.item_pristine_quantity
        item.item_damaged_quantity = unreturned_items.item_borrowed.item_stock.item_damaged_quantity
        item.item_borrowed_quantity = unreturned_items.item_borrowed.item_stock.item_borrowed_quantity
        item.save()

        unreturned_items.delete()


        return JsonResponse({'success': True})
    
    else:
        return JsonResponse({'error': 'Invalid form submission'}, status=400)