from django.shortcuts import render
from home.decorators import allowed_users
from django.contrib.auth.models import User
from rest_framework import serializers
from django.http import JsonResponse
from recents.models import *
from unreturned.models import *
from home.models import *
from django.core.exceptions import ObjectDoesNotExist

import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 
        depth = 1  

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  

class StockSerializer(serializers.ModelSerializer):
    item_information = ItemSerializer()  

    class Meta:
        model = Stock
        fields = '__all__' 

class HistorySerializer(serializers.ModelSerializer):
    item_stock = StockSerializer()
    class Meta:
        model = Borrowed_Item
        fields = '__all__'  
        depth = 1 
        
class UnreturnedSerializer(serializers.ModelSerializer):
    item_borrowed = HistorySerializer()
    class Meta:
        model = Unreturned_Item
        fields = '__all__' 
        depth = 1

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
        return JsonResponse({'error': 'User not found'}, status=404)
    
def get_user_history(request):
    user_pk = request.GET.get('user_id')
    try:
        user_history = Borrowed_Item.objects.filter(item_borrower=user_pk)
        serialized_data = HistorySerializer(user_history, many=True).data
        
        return JsonResponse({'user_history': serialized_data})
    
    except ObjectDoesNotExist:
        
        return JsonResponse({'error': 'User not found'}, status=404)
    
def get_user_unreturned(request):
    user_pk = request.GET.get('user_id')
    try:
        user_history = Unreturned_Item.objects.filter(item_borrowed__item_borrower=user_pk)
        serialized_data = UnreturnedSerializer(user_history, many=True).data
        
        return JsonResponse({'user_unreturned': serialized_data})
    
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)