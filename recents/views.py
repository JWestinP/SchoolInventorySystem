from django.shortcuts import render
from django.http import HttpResponse
from unreturned.models import *
from .models import *
from home.models import *
from home.decorators import allowed_users
from django.db.models import Q  # Import Q for complex queries

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

@allowed_users(allowed_roles=['Admin'])
def admin_search_recents(request):
    query = request.GET.get('q', '')

    if query:
        # Adjust this query based on your model relationships
        items = Borrowed_Item.objects.filter(
            Q(item_stock__item_information__item_name__icontains=query) |
            Q(item_borrower__username__icontains=query)  # Assuming the borrower's username is relevant
        )
    else:
        items = Borrowed_Item.objects.all()

    return render(request, 'recents/admin_recents.html', {'borrowed_item': items, 'query': query})

@allowed_users(allowed_roles=['Faculty'])
def faculty_search_recents(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        # Adjust this query based on your model relationships
        items = Borrowed_Item.objects.filter(
            Q(item_stock__item_information__item_name__icontains=query) |
            Q(item_borrower__username__icontains=query)  # Assuming the borrower's username is relevant
        )
    else:
        items = Borrowed_Item.objects.filter(item_borrower=user)

    return render(request, 'recents/recents.html', {'borrowed_item': items, 'query': query})

