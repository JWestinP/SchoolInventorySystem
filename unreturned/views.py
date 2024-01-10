from django.shortcuts import render
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
