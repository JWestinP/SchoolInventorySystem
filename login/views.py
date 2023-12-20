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
            return redirect('home')
        
        else:
            messages.error(request, "Invalid email or password, please try again.")
            return redirect('login')
    
    return render(request, 'login/login.html')
