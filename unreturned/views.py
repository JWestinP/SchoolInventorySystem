from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from recents.models import *
from home.models import *
from datetime import datetime
from home.decorators import allowed_users
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowed_Item
        fields = '__all__' 
        depth = 1  

class UnreturnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unreturned_Item
        fields = '__all__' 
        depth = 1  

@allowed_users(allowed_roles=['Faculty'])
def unreturned(request):
    user = request.user
    unreturned_items = Unreturned_Item.objects.filter(item_borrowed__item_borrower = user)

    return render(request, 'unreturned/unreturned.html',
                {'unreturned_items': unreturned_items})

@allowed_users(allowed_roles=['Admin'])
def admin_unreturned(request):
    unreturned_items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html',
                {'unreturned_items': unreturned_items})

def get_borrow_info(request):
    borrow_pk = request.GET.get('borrow_id')
    
    try:
        borrow_info = Borrowed_Item.objects.get(borrow_form_id=borrow_pk)
        unreturned_info = Unreturned_Item.objects.get(item_borrowed=borrow_pk)
        serialized_data = BorrowSerializer(borrow_info).data
        unreturned_serialized_data = UnreturnedSerializer(unreturned_info).data
        return JsonResponse({'borrowed_info': serialized_data,
                             'unreturned_info': unreturned_serialized_data,})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
def get_return_form(request):
    return_form = ReturnForm()
    form_html = render_to_string('unreturned/return_form.html', {'return_form': return_form}, request=request)
    return JsonResponse({'form_html' : form_html})

@login_required
def save_return_form(request):
    return_form = ReturnForm(request.POST)
    stock_id = request.POST.get('stock_id')
    unreturned_id = request.POST.get('unreturned_id')
    borrowed_id = request.POST.get('borrowed_id')
    if return_form.is_valid():
        borrowed_id = int(borrowed_id)
        borrowed_instance = get_object_or_404(Borrowed_Item, borrow_form_id=borrowed_id)
        
        item_borrowed_value = borrowed_instance.item_quantity
        total_returned = return_form.cleaned_data['item_pristine_quantity'] + return_form.cleaned_data['item_damaged_quantity']
        if item_borrowed_value == total_returned:
            pristine_quantity = return_form.cleaned_data['item_pristine_quantity']
            damaged_quantity = return_form.cleaned_data['item_damaged_quantity']
            stock_id = int(stock_id)
            unreturned_id = int(unreturned_id)
            stock_instance = get_object_or_404(Stock, pk=stock_id)
            unreturned_instance = get_object_or_404(Unreturned_Item, pk=unreturned_id)
            stock_instance.item_current_quantity += pristine_quantity
            stock_instance.item_pristine_quantity += pristine_quantity
            stock_instance.item_borrowed_quantity -= item_borrowed_value
            stock_instance.item_damaged_quantity += damaged_quantity
        
            stock_instance.save()
            
            unreturned_instance.delete()
            print('updated current count')

            # Return a success response
            return JsonResponse({'message': 'Form submitted successfully'})
        
        else:
            print('Form is NOT valid! Borrowed value greater than current stock')
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    else:
        print('Form is NOT valid!')
        print('Errors:', return_form.errors.as_data())

        return JsonResponse({'error': 'Invalid form submission'}, status=400)

@allowed_users(allowed_roles=['Admin'])
def admin_search_unreturned(request):
    query = request.GET.get('q', '')

    if query:
        # Adjust this query based on your model relationships
        items = Unreturned_Item.objects.filter(
            Q(item_borrowed__item_stock__item_information__item_name__icontains=query) |
            Q(item_borrowed__item_borrower__username__icontains=query)
        )
    else:
        items = Unreturned_Item.objects.all()

    return render(request, 'unreturned/admin_unreturned.html', {'unreturned_items': items, 'query': query})


@allowed_users(allowed_roles=['Faculty'])
def faculty_search_unreturned(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        # Adjust this query based on your model relationships
        items = Unreturned_Item.objects.filter(
            Q(item_borrowed__item_stock__item_information__item_name__icontains=query) |
            Q(item_borrowed__item_borrower__username__icontains=query)
        )
    else:
        items = Unreturned_Item.objects.filter(item_borrowed__item_borrower=user)

    return render(request, 'unreturned/unreturned.html', {'unreturned_items': items, 'query': query})