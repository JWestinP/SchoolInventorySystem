from django.shortcuts import render

# Create your views here.
def userprofile(request):
    return render(request, ('userprofile/userprofile.html'))

def admin_userprofile(request):
    return render(request, ('userprofile/admin_userprofile.html'))