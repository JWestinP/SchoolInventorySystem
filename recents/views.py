from django.shortcuts import render
from django.http import HttpResponse
from unreturned.models import *
from .models import *
from home.models import *
from home.decorators import allowed_users

# Create your views here.
@allowed_users(allowed_roles=['Faculty'])
def recents(request):
    user = request.user
    # item = Item.objects.filter(item_borrowed__item_borrower = user)
    borrowed_item = Borrowed_Item.objects.filter(item_borrower = user)

    item = Item.objects.all()
    # borrowed_item = Borrowed_Item.objects.all()

    return render(request, ('recents/recents.html'),
                {'borrowed_item': borrowed_item,
                'item': item})

@allowed_users(allowed_roles=['Admin'])
def admin_recents(request):
    item = Item.objects.all()
    borrowed_item = Borrowed_Item.objects.all()

    return render(request, ('recents/admin_recents.html'),
                {'borrowed_item': borrowed_item,
                'item': item})
