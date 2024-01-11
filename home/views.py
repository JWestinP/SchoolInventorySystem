from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import *
from .forms import BorrowForm
from recents.models import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.apps import apps
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from .models import Item, Category

# Create your views here.
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  # Include all fields
        depth = 1  # Include one level of related objects

@login_required
def admin_home(request):
    return render(request, ('home/admin_home.html'))

@login_required
def guest_home(request):
    return render(request, ('home/guest_home.html'))

@login_required
def home(request):
    current_user = request.user
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'

    # Initialize queryset variables
    furniture_items = room_items = cleaning_material_items = technology_items = dean_approval_items = None

    # If a search query is provided
    # if query:
    #     try:
    #         query_int = int(query)
    #         furniture_items = Furniture.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
    #         room_items = Room.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
    #         cleaning_material_items = Cleaning_Material.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
    #         technology_items = Technology.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
    #         dean_approval_items = Dean_Approval_Needed_Item.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
    #     except ValueError:
    #         furniture_items = Furniture.objects.filter(item_name__icontains=query)
    #         room_items = Room.objects.filter(item_name__icontains=query)
    #         cleaning_material_items = Cleaning_Material.objects.filter(item_name__icontains=query)
    #         technology_items = Technology.objects.filter(item_name__icontains=query)
    #         dean_approval_items = Dean_Approval_Needed_Item.objects.filter(item_name__icontains=query)

    #         if query and query.lower() == "furniture":
    #             furniture_items = Furniture.objects.all()
    #         if query and query.lower() == "room":
    #             room_items = Room.objects.all()
    #         if query and query.lower() == "cleaning material":
    #             cleaning_material_items = Cleaning_Material.objects.all()
    #         if query and query.lower() == "technology":
    #             technology_items = Technology.objects.all()
    #         if query and query.lower() == "dean approval needed item":
    #             dean_approval_items = Dean_Approval_Needed_Item.objects.all()

    # cleaning_inventory = Cleaning_Material.objects.all()
    # gadget_inventory = Technology.objects.all()
    # furniture_inventory = Furniture.objects.all()
    # room_inventory = Room.objects.all()
    # dean_inventory = Dean_Approval_Needed_Item.objects.all()


    categories = Category.objects.all()
    borrow_form = BorrowForm()
    if request.method == 'POST':
        borrow_form = BorrowForm(request.POST)
        if borrow_form.is_valid():
            model_instance = borrow_form.save(commit=False)
            model_instance.item_borrower = current_user
            model_instance.save()

        else:
            borrow_form = BorrowForm()


    return render(request, 'home/home.html', {
        'furniture_items' : furniture_items,
        'room_items' : room_items,
        'cleaning_material_items' : cleaning_material_items,
        'technology_items' : technology_items,
        'dean_approval_items' : dean_approval_items,
        'query' : query,
        'borrow_form' : borrow_form,
        'categories' : categories,
        # 'cleaning_inventory' : cleaning_inventory,
        # 'gadget_inventory' : gadget_inventory,
        # 'furniture_inventory' : furniture_inventory,
        # 'room_inventory' : room_inventory,
        # 'dean_inventory' : dean_inventory,
    })

def get_borrow_form(request):
    borrow_form = BorrowForm()
    form_html = render_to_string('home/borrow_form.html', {'borrow_form': borrow_form}, request=request)
    return JsonResponse({'form_html': form_html})

def get_items(request):
    category = request.GET.get('category')
    print(category)
    try:
        if category is not None and category != 'null':
            # Your existing logic here
            items = Item.objects.filter(item_category__item_category=category)

            # Use the serializer to serialize the queryset
            serializer = ItemSerializer(items, many=True)
            serialized_data = serializer.data

            return JsonResponse({'items': serialized_data})
        else:
            raise ValueError('Invalid category parameter in the request.')
    except Exception as e:
        # Log the exception for debugging purposes
        print(f'Error in your_ajax_view: {e}')
        return JsonResponse({'error': 'Internal server error'}, status=500)

@login_required
def save_borrow_form(request):
    current_user = request.user
    borrow_form = BorrowForm(request.POST)
    stock_id = request.POST.get('stock_id')

    
    if borrow_form.is_valid():
        model_instance = borrow_form.save(commit=False)
        model_instance.item_borrower = current_user
        model_instance.save()
        
        stock_id = int(stock_id)

        stock_instance = get_object_or_404(Stock, pk=stock_id)
        borrowed_count = model_instance.item_quantity
        stock_instance.item_current_quantity -= borrowed_count
        stock_instance.item_borrowed_quantity += borrowed_count
        
        
        stock_instance.save()
        print('updated current count')

        # Return a success response
        return JsonResponse({'message': 'Form submitted successfully'})

    else:
        print('Form is NOT valid!')
        print('Errors:', borrow_form.errors.as_data())

        # Print the choices for the item_stock field
        item_stock_choices = BorrowForm.base_fields['item_stock'].queryset.values_list('pk', flat=True)
        print('Choices for item_stock:', item_stock_choices)

        return JsonResponse({'error': 'Invalid form submission'}, status=400)

def get_item_inventory(request):
    item_inventory = Stock.objects.all()

    # Convert each Item to a dictionary
    items_data = [{'item_id' : item.item_information.item_id,
                   'item_name' : item.item_information.item_name,
                   'item_category' : item.item_information.item_category.item_category,
                   'item_description' : item.item_information.item_description,
                   'item_photo' : item.item_information.item_photo.url,
                   'item_total' : item.item_total_quantity,
                   'item_current' : item.item_current_quantity,
                   'item_borrowed' : item.item_borrowed_quantity,
                   'stock_id' : item.pk} for item in item_inventory]
    print(items_data)
    return JsonResponse({'items': items_data}, safe=False)

def search_items(request):
    query = request.GET.get('q')

    if query:
        # Perform a case-insensitive search on the item name, category, and item id
        results = Item.objects.filter(
            models.Q(item_name__icontains=query) |
            models.Q(item_category__item_category__icontains=query) |
            models.Q(item_id__icontains=query)
        )
    else:
        return redirect('home')

    return render(request, 'home/home.html', {'results': results, 'query': query})

