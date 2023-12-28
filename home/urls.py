from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('guest_home', views.guest_home, name='guest_home'),
    path('api/cleaning_inventory/', views.get_cleaning_inventory, name='get_cleaning_inventory'),
    path('api/furniture_inventory/', views.get_furniture_inventory, name='get_furniture_inventory'),
    path('api/technology_inventory/', views.get_technology_inventory, name='get_technology_inventory'),
    path('api/room_inventory/', views.get_room_inventory, name='get_room_inventory'),
    path('api/dean_inventory/', views.get_dean_inventory, name='get_dean_inventory'),
    path('get_borrow_form/', views.get_borrow_form, name='get_borrow_form'),
    path('save_borrow_form/<str:model_class_name>/', views.save_borrow_form, name='save_borrow_form'),
]