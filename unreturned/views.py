from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from recents.models import *
from home.models import *

# Create your views here.
# test
def show_unreturned_items(request):
    # return HttpResponse("This is where unreturned items should show.")

    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

def admin_unreturned(request):
    return render(request, ('unreturned/admin_unreturned.html'))
