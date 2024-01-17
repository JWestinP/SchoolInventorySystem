from django.shortcuts import render
from home.decorators import allowed_users
from django.contrib.auth.models import User

# Create your views here.

@allowed_users(allowed_roles=['Admin'])
def members(request):
    faculty = User.objects.all()
    return render(request, ('members/members.html'),{'faculty': faculty})