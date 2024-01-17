from django.shortcuts import render
from home.decorators import allowed_users
# Create your views here.

@allowed_users(allowed_roles=['Admin'])
def members(request):
    return render(request, ('members/members.html'))