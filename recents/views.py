from django.shortcuts import render
from home.decorators import allowed_users

# Create your views here.
@allowed_users(allowed_roles=['Faculty'])
def recents(request):
    return render(request, ('recents/recents.html'))

@allowed_users(allowed_roles=['Admin'])
def admin_recents(request):
    return render(request, ('recents/admin_recents.html'))