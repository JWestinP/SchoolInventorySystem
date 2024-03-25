from .decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
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

def guest_login(request):
    return redirect('guest_home')

def user_guest(request):
    pass

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "forget_password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="forget_password/password_reset.html", context={"password_reset_form":password_reset_form})