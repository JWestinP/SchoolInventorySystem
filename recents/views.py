from django.shortcuts import render
from django.http import HttpResponse
from unreturned.models import *
from .models import *
from home.models import *

# Create your views here.
def recents(request):
    item = Item.objects.all()
    borrowed_item = Borrowed_Item.objects.all()

    return render(request, ('recents/recents.html'),
                {'borrowed_item': borrowed_item,
                'item': item})

def admin_recents(request):
    return render(request, ('recents/admin_recents.html'))
