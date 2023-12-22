from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, ('home/home.html'))

def admin_home(request):
    return render(request, ('home/admin_home.html'))

def guest_home(request):
    return render(request, ('home/guest_home.html'))

