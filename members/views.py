from django.shortcuts import render
from home.decorators import allowed_users
from django.contrib.auth.models import User
from rest_framework import serializers
from django.http import JsonResponse
from recents.models import *
from unreturned.models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields
        depth = 1  # Include one level of related objects

@allowed_users(allowed_roles=['Admin'])
def members(request):
    faculty = User.objects.all()
    return render(request, ('members/members.html'),{'faculty': faculty})

def get_user_info(request):
    user_pk = request.GET.get('user_id')
    
    try:
        user_info = User.objects.get(id=user_pk)
        serialized_data = UserSerializer(user_info).data
        user_recents_total = Borrowed_Item.objects.filter(item_borrower=user_info).count()
        user_unreturned_total = Unreturned_Item.objects.filter(item_borrowed__item_borrower=user_info).count()
        
        return JsonResponse({'user': serialized_data,
                             'total_recents': user_recents_total,
                             'total_unreturned': user_unreturned_total})
    except ObjectDoesNotExist:
        # Handle the case where the user with the specified ID doesn't exist
        return JsonResponse({'error': 'User not found'}, status=404)