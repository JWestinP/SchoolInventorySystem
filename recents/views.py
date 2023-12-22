from django.shortcuts import render

# Create your views here.
def recents(request):
    return render(request, ('recents/recents.html'))

def admin_recents(request):
    return render(request, ('recents/admin_recents.html'))