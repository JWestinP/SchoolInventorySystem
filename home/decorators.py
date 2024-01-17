from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = []
            if request.user.groups.exists():
                groups = list(request.user.groups.values_list('name', flat=True)[:2])
                
            if any(group in allowed_roles for group in groups):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You don't have permission to access this page.")
        return wrapper_func
    return decorator