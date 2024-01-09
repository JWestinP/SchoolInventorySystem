from django.shortcuts import render
from recents.models import Borrowed_Item
from unreturned.models import Unreturned_Item

from datetime import timedelta, date, datetime
from django.utils import timezone

# Create your views here.
def notification(request):
    unreturned_items = get_unreturned_items_info(request)
    unreturned_item_exist = check(request)
    print("unreturned_item_exist", unreturned_item_exist)
    
    context = {'unreturned_item_exist' : unreturned_item_exist, 'unreturned_items' : unreturned_items}
    print ("Context" , context)
    
    return render(request, 'notification/notification.html', context)

def check (request):
    user = request.user
    today = datetime.now().date()
    
    queryset = Unreturned_Item.objects.filter(item_borrowed__item_borrower = user,)
    unreturned_item_exist = queryset.exists()
    return unreturned_item_exist

def get_unreturned_items_info(request):
    user = request.user
    queryset = Unreturned_Item.objects.filter(item_borrowed__item_borrower=user)
    
    unreturned_items_info = [
        {
            'item_name': item.item_borrowed.item_stock,
            'item_days_not_returned': (timezone.now().date() - item.item_borrowed.item_date_borrowed).days,
            'item_date_borrowed': item.item_borrowed.item_date_borrowed,
        }
        for item in queryset
    ]
    
    return unreturned_items_info
