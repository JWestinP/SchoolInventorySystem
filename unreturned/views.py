from django.shortcuts import render
from django.http import HttpResponse
from .models import Unreturned_Item

# Create your views here.
# test
def show_unreturned_items(request):
    # return HttpResponse("This is where unreturned items should show.")

    unreturned_items = Unreturned_Item.objects.all()
    return render(request, 'templates/unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})
