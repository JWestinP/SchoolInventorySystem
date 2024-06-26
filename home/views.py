from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import *
from .forms import *
from recents.models import *
from unreturned.models import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.apps import apps
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from .models import Item, Category
from .decorators import allowed_users

#Model serializers in charge of getting data from models for JS
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  
        depth = 1  
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 
        depth = 1  

#For initializing admin home
@login_required
@allowed_users(allowed_roles=['Admin'])
def admin_home(request):
    current_user = request.user
    borrow_form = BorrowForm()
    if request.method == 'POST':
        borrow_form = BorrowForm(request.POST)
        if borrow_form.is_valid():
            model_instance = borrow_form.save(commit=False)
            model_instance.item_borrower = current_user
            model_instance.save()
        else:
            borrow_form = BorrowForm()
    
    categories = Category.objects.all()
    return render(request, ('home/admin_home.html'), {
        'borrow_form' : borrow_form,
        'categories' : categories,
    })

#For initializing guest home
def guest_home(request):   
    categories = Category.objects.all()
    return render(request, ('home/guest_home.html'), {
        'categories' : categories,
    })

#For initializing faculty home
@login_required
@allowed_users(allowed_roles=['Faculty'])
def home(request):
    current_user = request.user
    borrow_form = BorrowForm()
    if request.method == 'POST':
        borrow_form = BorrowForm(request.POST)
        if borrow_form.is_valid():
            model_instance = borrow_form.save(commit=False)
            model_instance.item_borrower = current_user
            model_instance.save()

        else:
            borrow_form = BorrowForm()
    categories = Category.objects.all()
    return render(request, 'home/home.html', {
        'borrow_form' : borrow_form,
        'categories' : categories,
    })

#For passing the category information to the JS
def get_category(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    serializer_data = serializer.data
    
    return JsonResponse({'categories' : serializer_data})

#For passing the item list to the JS
def get_items(request):
    category = request.GET.get('category')
    try:
        if category is not None and category != 'null':
            items = Item.objects.filter(item_category__item_category=category)

            serializer = ItemSerializer(items, many=True)
            serialized_data = serializer.data

            return JsonResponse({'items': serialized_data})
        else:
            raise ValueError('Invalid category parameter in the request.')
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

#For fetching the item information
def get_item_inventory(request):
    item_inventory = Stock.objects.all()

    items_data = [{'item_id' : item.item_information.item_id,
                   'item_name' : item.item_information.item_name,
                   'item_category' : item.item_information.item_category.item_category,
                   'item_description' : item.item_information.item_description,
                   'item_photo' : item.item_information.item_photo.url,
                   'item_total' : item.item_total_quantity,
                   'item_pristine' : item.item_pristine_quantity,
                   'item_damaged' : item.item_damaged_quantity,
                   'item_current' : item.item_current_quantity,
                   'item_borrowed' : item.item_borrowed_quantity,
                   'item_one_time_borrow' : item.item_information.item_one_time_borrow,
                   'stock_id' : item.pk} for item in item_inventory]
    return JsonResponse({'items': items_data}, safe=False)

#For passing the borrow form to the JS
def get_borrow_form(request):
    borrow_form = BorrowForm()
    form_html = render_to_string('home/borrow_form.html', {'borrow_form': borrow_form}, request=request)
    return JsonResponse({'form_html' : form_html})

#For passing the borrow form to the JS
def get_guest_borrow_form(request):
    borrow_form = BorrowForm()
    user_form = UserForm()
    
    form_html = render_to_string('home/guest_borrow_form.html', {
        'borrow_form': borrow_form,
        'user_form': user_form
    }, request=request)
    
    return JsonResponse({'form_html': form_html})

#For passing the item addition form to the JS
def get_item_form(request):
    item_form = ItemForm()
    item_form_html = render_to_string('home/item_form.html', {'item_form': item_form}, request=request)
    return JsonResponse({'item_form_html' : item_form_html})

#For passing the stock addition form to the JS
def get_stock_form(request):
    stock_form = StockForm()
    stock_form_html = render_to_string('home/stock_form.html', {'stock_form': stock_form}, request=request)
    return JsonResponse({'stock_form_html' : stock_form_html})

#For passing the category addition form to the JS
def get_category_form(request):
    category_form = CategoryForm()
    category_form_html = render_to_string('home/category_form.html', {'category_form': category_form}, request=request)
    return JsonResponse({'category_form_html' : category_form_html})

#For saving the borrow form instance
@login_required
def save_borrow_form(request):
    current_user = request.user
    borrow_form = BorrowForm(request.POST)
    stock_id = request.POST.get('stock_id')
    stock_instance = get_object_or_404(Stock, pk=stock_id)
    item_check = stock_instance.item_information.item_one_time_borrow
    already_borrowed = False
    if item_check:
        borrowed_check = Unreturned_Item.objects.filter(item_borrowed__item_borrower = current_user).exists()
        if borrowed_check:
            already_borrowed = True
            
    if borrow_form.is_valid():
        item_borrowed_value = borrow_form.cleaned_data['item_quantity']
        if item_borrowed_value <= stock_instance.item_current_quantity and item_borrowed_value <= stock_instance.item_pristine_quantity and already_borrowed == False:

            model_instance = borrow_form.save(commit=False)
            model_instance.item_borrower = current_user
            model_instance.save()
            
            stock_id = int(stock_id)

            stock_instance = get_object_or_404(Stock, pk=stock_id)
            borrowed_count = model_instance.item_quantity
            stock_instance.item_current_quantity -= borrowed_count
            stock_instance.item_pristine_quantity -= borrowed_count
            stock_instance.item_borrowed_quantity += borrowed_count
        
            stock_instance.save()
            
            unreturned_instance = Unreturned_Item.objects.create(item_borrowed = model_instance, item_days_not_returned = 0)
            unreturned_instance.save()

            return JsonResponse({'message': 'Item has been borrowed successfully'})
        
        else:
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

#For saving the guest borrow form instance
def guest_save_borrow_form(request):
    borrow_form = BorrowForm(request.POST)
    user_form = UserForm(request.POST)
    
    stock_id = request.POST.get('stock_id')
    stock_instance = get_object_or_404(Stock, pk=stock_id)

    if borrow_form.is_valid() and user_form.is_valid():
        item_borrowed_value = borrow_form.cleaned_data['item_quantity']
        
        if item_borrowed_value <= stock_instance.item_current_quantity and item_borrowed_value <= stock_instance.item_pristine_quantity:
            borrow_instance = borrow_form.save(commit=False)
            
            user_id = user_form.cleaned_data['user'].id

            user = User.objects.get(id=user_id)
            
            borrow_instance.item_borrower = user 
            borrow_instance.save()
            
            stock_instance.item_current_quantity -= item_borrowed_value
            stock_instance.item_pristine_quantity -= item_borrowed_value
            stock_instance.item_borrowed_quantity += item_borrowed_value
            stock_instance.save()
            
            unreturned_instance = Unreturned_Item.objects.create(item_borrowed=borrow_instance, item_days_not_returned=0)
            unreturned_instance.save()

            return JsonResponse({'message': 'Item has been borrowed successfully'})
        else:
            return JsonResponse({'error': 'Invalid form submission'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

#For saving the item addition form instance
def save_item_form(request):
    item_form = ItemForm(request.POST, request.FILES)
    
    if item_form.is_valid():
        model_instance = item_form.save(commit=False)
        model_instance.save()
        
        request.session['item'] = model_instance.item_id
        return JsonResponse({'message': 'Added new item successfully'})

    else:
       
        return JsonResponse({'error': 'Invalid form submission'}, status=400)
    
#For saving the stock addition form instance
def save_stock_form(request):
    stock_form = StockForm(request.POST)
    specific_item = request.session.get('item')
    if stock_form.is_valid():
        item_instance = get_object_or_404(Item, item_id = specific_item)
        model_instance = stock_form.save(commit=False)
        model_instance.item_current_quantity = model_instance.item_pristine_quantity
        
        model_instance.item_borrowed_quantity = 0
        model_instance.item_information = item_instance
        model_instance.save()
        
        del request.session['item']
        return JsonResponse({'message': 'Added new stock to item successfully'})

    else:
      
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

#For saving the category addition form instance
def save_category_form(request):
    category_form = CategoryForm(request.POST, request.FILES)
    
    if category_form.is_valid():
        model_instance = category_form.save(commit=False)
        model_instance.save()
        return JsonResponse({'message': 'Category added successfully'})

    else:
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

#For deleting an item instance
def delete_item(request):
    item_pk = request.GET.get('item_id', None)

    if item_pk is not None:
        Item.objects.filter(item_id=item_pk).delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    else:
        return JsonResponse({'message': 'Item ID not provided'}, status=400)

#For deleting a category instance
def delete_category(request):
    category_pk = request.GET.get('category_id', None)

    if category_pk is not None:
        Category.objects.filter(id=category_pk).delete()
        return JsonResponse({'message': 'Category deleted successfully'})
    else:
        return JsonResponse({'message': 'Category ID not provided'}, status=400)    
    
#For searching items in faculty
def search_items(request):
    query = request.GET.get('q')

    if query:
        results = Item.objects.filter(
            models.Q(item_name__icontains=query) |
            models.Q(item_category__item_category__icontains=query) |
            models.Q(item_id__icontains=query)
        )
    else:
        return redirect('home')

    return render(request, 'home/home.html', {'results': results, 'query': query})

#For searching items in admin
def search_items_admin(request):
    query = request.GET.get('q')

    if query:
        results = Item.objects.filter(
            models.Q(item_name__icontains=query) |
            models.Q(item_category__item_category__icontains=query) |
            models.Q(item_id__icontains=query)
        )
    else:
        return redirect('admin_home')

    return render(request, 'home/admin_home.html', {'results': results, 'query': query})

#For searching items in guest
def search_items_guest(request):
    query = request.GET.get('q')

    if query:
        results = Item.objects.filter(
            models.Q(item_name__icontains=query) |
            models.Q(item_category__item_category__icontains=query) |
            models.Q(item_id__icontains=query)
        )
    else:
        return redirect('guest_home')

    return render(request, 'home/guest_home.html', {'results': results, 'query': query})

