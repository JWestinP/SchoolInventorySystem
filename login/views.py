from .decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

# Create your views here.
@unauthenticated_user
@never_cache
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(username = email, password = password)
        
        if user is not None:
            login(request, user)
            group_names = []
            if user.groups.exists():
                group_names = user.groups.values_list('name', flat=True)[:1]  # Get the first two group names
                
            if 'Admin' in group_names:
                return redirect('admin_home')  
            elif 'Faculty' in group_names:
                return redirect('home')
        
        else:
            messages.error(request, "Invalid email or password, please try again.")
            return redirect('login')
    
    return render(request, 'login/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You've successfully logged out.")
    return redirect('login')