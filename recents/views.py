from django.shortcuts import render
from django.http import HttpResponse
from unreturned.models import Unreturned_Item
from .models import *
from home.models import *

# Create your views here.
def recents(request):
    return render(request, ('recents/recents.html'))

def admin_recents(request):
    return render(request, ('recents/admin_recents.html'))