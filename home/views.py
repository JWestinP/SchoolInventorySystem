from django.shortcuts import render
from django.db.models import Q
from .models import Furniture, Room, Cleaning_Material, Technology, Dean_Approval_Needed_Item

# Create your views here.
def home(request):
    return render(request, ('home/home.html'))

def admin_home(request):
    return render(request, ('home/admin_home.html'))

def guest_home(request):
    return render(request, ('home/guest_home.html'))

# myapp/views.py
def home(request):
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
    
    return render(request, 'home/home.html', {
        'furniture_items': furniture_items,
        'room_items': room_items,
        'cleaning_material_items': cleaning_material_items,
        'technology_items': technology_items,
        'dean_approval_items': dean_approval_items,
        'query': query,
        'cleaning_inventory' : cleaning_inventory,
        'gadget_inventory' : gadget_inventory,
        'furniture_inventory' : furniture_inventory,
        'room_inventory' : room_inventory,
        'dean_inventory' : dean_inventory,
    })

