from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from home.decorators import allowed_users


# Create your views here.

#For initializing faculty profile tab
@login_required
@allowed_users(allowed_roles=['Faculty'])
def userprofile(request):
    user_profile = Profile.objects.get(user=request.user) 

    return render(request, 'userprofile/userprofile.html',{'user_profile': user_profile})

#For initializing admin profile tab
@login_required
@allowed_users(allowed_roles=['Admin'])
def admin_userprofile(request):
    user_profile = Profile.objects.get(user=request.user) 
    return render(request, 'userprofile/admin_userprofile.html',{'user_profile': user_profile})

#For initializing faculty edit profile tab
@login_required
@allowed_users(allowed_roles=['Faculty'])
def editprofile(request):
    user_profile = request.user.profile


    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')

            if request.user.groups.filter(name='Admin').exists():
                return redirect('admin_userprofile')
            else:
                return redirect('userprofile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'userprofile/editprofile.html', context)

#For initializing admin edit profile tab
@login_required
@allowed_users(allowed_roles=['Admin'])
def editprofile_admin(request):

    user_profile = request.user.profile


    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')

            if request.user.groups.filter(name='Admin').exists():
                return redirect('admin_userprofile')
            else:
                return redirect('userprofile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'userprofile/editprofileadmin.html', context)
