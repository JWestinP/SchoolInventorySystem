from django.shortcuts import render
from home.decorators import allowed_users

# Create your views here.
@allowed_users(allowed_roles=['Faculty'])
def userprofile(request):
    return render(request, ('userprofile/userprofile.html'))

@allowed_users(allowed_roles=['Admin'])
def admin_userprofile(request):
    return render(request, ('userprofile/admin_userprofile.html'))