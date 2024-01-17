from django.shortcuts import render
from django.http import HttpResponse
from .models import Unreturned_Item
from home.decorators import allowed_users

# Create your views here.
# test
@allowed_users(allowed_roles=['Faculty'])
def show_unreturned_items(request):
    # return HttpResponse("This is where unreturned items should show.")

    unreturned_items = Unreturned_Item.objects.all()
    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

@allowed_users(allowed_roles=['Admin'])
def admin_unreturned(request):
    return render(request, ('unreturned/admin_unreturned.html'))
