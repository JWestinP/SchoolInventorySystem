from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from home.decorators import allowed_users

# Create your views here.
@login_required
@allowed_users(allowed_roles=['Faculty'])
def userprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            print("User form saved successfully!")
            p_form.save()
            print("Profile form saved successfully!")

            messages.success(request, f'Your account has been updated!')
            return redirect('userprofile')
        else:
            print("Form is not valid. Errors:", u_form.errors, p_form.errors)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'userprofile/userprofile.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def admin_userprofile(request):
    user_profile = Profile.objects.get(user=request.user) 
    return render(request, 'userprofile/admin_userprofile.html',{'user_profile': user_profile})

@login_required
def editprofile(request):
    # Retrieve the user's profile
    #user_profile = User.objects.get(pk=request.user.id).profile
    user_profile = request.user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('userprofile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'userprofile/editprofile.html', context)
