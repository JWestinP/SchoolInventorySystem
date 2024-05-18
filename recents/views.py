from django.shortcuts import render
from django.http import HttpResponse
from unreturned.models import *
from .models import *
from home.models import *
from home.decorators import allowed_users
from django.db.models import Q  

@allowed_users(allowed_roles=['Faculty'])
def recents(request):
    user = request.user
    borrowed_item = Borrowed_Item.objects.filter(item_borrower = user)

    item = Item.objects.all()

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

@allowed_users(allowed_roles=['Admin'])
def admin_search_recents(request):
    query = request.GET.get('q', '')

    if query:
        items = Borrowed_Item.objects.filter(
            Q(item_stock__item_information__item_name__icontains=query) |
            Q(item_borrower__username__icontains=query)   
        )
    else:
        items = Borrowed_Item.objects.all()

    return render(request, 'recents/admin_recents.html', {'borrowed_item': items, 'query': query})

@allowed_users(allowed_roles=['Faculty'])
def faculty_search_recents(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        items = Borrowed_Item.objects.filter(
            Q(item_stock__item_information__item_name__icontains=query) |
            Q(item_borrower__username__icontains=query)  
        )
    else:
        items = Borrowed_Item.objects.filter(item_borrower=user)

    return render(request, 'recents/recents.html', {'borrowed_item': items, 'query': query})

