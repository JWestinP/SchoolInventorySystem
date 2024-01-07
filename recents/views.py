from django.shortcuts import render
from django.http import HttpResponse
from unreturned.models import *
from .models import *
from home.models import *

# Create your views here.
def recents(request):
    return render(request, ('recents/recents.html'))

def admin_recents(request):
    return render(request, ('recents/admin_recents.html'))

def show_recents_items(request):
    category = Category.objects.all()
    item = Item.ojects.all()
    stock = Stock.objects.all()
    borrowed_item = Borrowed_Item.objects.all()
    unretunrned_item = Unreturned_Item.objects.all()

    recents_items = [category, item, stock, borrowed_item, unretunrned_item]

    return render(request, 'recents/recents.html',
                {'recents_items': recents_items})