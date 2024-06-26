from django.http import HttpResponse
from django.shortcuts import redirect

#Decorator in charge of checking user's group
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Admin':
                return redirect('admin_home')
            elif group == 'Faculty':
                return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func