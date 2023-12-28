from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Furniture, Room, Cleaning_Material, Technology, Dean_Approval_Needed_Item
from .forms import BorrowForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.apps import apps
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def admin_home(request):
    return render(request, ('home/admin_home.html'))

@login_required
def guest_home(request):
    return render(request, ('home/guest_home.html'))

# myapp/views.py
@login_required
def home(request):
    current_user = request.user
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'

    # Initialize queryset variables
    furniture_items = room_items = cleaning_material_items = technology_items = dean_approval_items = None

    # If a search query is provided
    if query:
        try:
            query_int = int(query)
            furniture_items = Furniture.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
            room_items = Room.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
            cleaning_material_items = Cleaning_Material.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
            technology_items = Technology.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
            dean_approval_items = Dean_Approval_Needed_Item.objects.filter(Q(item_name__icontains=query) | Q(item_id=query_int))
        except ValueError:
            furniture_items = Furniture.objects.filter(item_name__icontains=query)
            room_items = Room.objects.filter(item_name__icontains=query)
            cleaning_material_items = Cleaning_Material.objects.filter(item_name__icontains=query)
            technology_items = Technology.objects.filter(item_name__icontains=query)
            dean_approval_items = Dean_Approval_Needed_Item.objects.filter(item_name__icontains=query)
            
            if query and query.lower() == "furniture":
                furniture_items = Furniture.objects.all()
            if query and query.lower() == "room":
                room_items = Room.objects.all()
            if query and query.lower() == "cleaning material":
                cleaning_material_items = Cleaning_Material.objects.all()
            if query and query.lower() == "technology":
                technology_items = Technology.objects.all()
            if query and query.lower() == "dean approval needed item":
                dean_approval_items = Dean_Approval_Needed_Item.objects.all()

    cleaning_inventory = Cleaning_Material.objects.all()
    gadget_inventory = Technology.objects.all()
    furniture_inventory = Furniture.objects.all()
    room_inventory = Room.objects.all()
    dean_inventory = Dean_Approval_Needed_Item.objects.all()
    
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
        'cleaning_inventory' : cleaning_inventory,
        'gadget_inventory' : gadget_inventory,
        'furniture_inventory' : furniture_inventory,
        'room_inventory' : room_inventory,
        'dean_inventory' : dean_inventory,
    })

def get_borrow_form(request):
    borrow_form = BorrowForm()
    form_html = render_to_string('home/borrow_form.html', {'borrow_form': borrow_form}, request=request)
    return JsonResponse({'form_html': form_html}) 

@login_required
def save_borrow_form(request, model_class_name):
    model_class = apps.get_model('home', model_class_name)
    
    current_user = request.user
    borrow_form = BorrowForm(request.POST)

    if borrow_form.is_valid():
        model_instance = borrow_form.save(commit=False)
        model_instance.item_borrower = current_user
        model_instance.save()

        if request.POST.get('copy_image') == 'true':
            source_item_id = request.POST.get('source_item_id')
            print('source_item_id received:', source_item_id)
            try:
                source_item = model_class.objects.get(pk=source_item_id)
                print('source_item retrieved successfully:', source_item)
                
                model_instance.item_photo = source_item.item_photo
                model_instance.save()
                
                if 'item_photo' in request.FILES:
                    print('item_photo received:', request.FILES['item_photo'])

                return JsonResponse({'message': 'Form data saved successfully'})
            
            except model_class.DoesNotExist:
                print(f'Source item with id {source_item_id} does not exist.')
                return JsonResponse({'error': 'Invalid source item id'}, status=400)

    else:
        print('Form is NOT valid!')
        print('Errors:', borrow_form.errors.as_data())
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

    return JsonResponse({'error': 'Invalid form submission'}, status=400)

def get_cleaning_inventory(request):
    cleaning_inventory = Cleaning_Material.objects.all().values()
    return JsonResponse(list(cleaning_inventory), safe=False)

def get_furniture_inventory(request):
    furniture_inventory = Furniture.objects.all().values()
    return JsonResponse(list(furniture_inventory), safe=False)

def get_room_inventory(request):
    room_inventory = Room.objects.all().values()
    return JsonResponse(list(room_inventory), safe=False)

def get_technology_inventory(request):
    technology_inventory = Technology.objects.all().values()
    return JsonResponse(list(technology_inventory), safe=False)

def get_dean_inventory(request):
    dean_inventory = Dean_Approval_Needed_Item.objects.all().values()
    return JsonResponse(list(dean_inventory), safe=False)