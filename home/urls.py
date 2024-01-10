from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('get_items/', views.get_items, name='get_items'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('guest_home', views.guest_home, name='guest_home'),
    path('api/item_inventory/', views.get_item_inventory, name='get_item_inventory'),
    path('get_borrow_form/', views.get_borrow_form, name='get_borrow_form'),
    path('get_item_form/', views.get_item_form, name='get_item_form'),
    path('get_stock_form/', views.get_stock_form, name='get_stock_form'),
    path('save_borrow_form/', views.save_borrow_form, name='save_borrow_form'),
    path('save_item_form/', views.save_item_form, name='save_item_form'),
    path('save_stock_form/', views.save_stock_form, name='save_stock_form'),
    path('delete_item/', views.delete_item, name='delete_item'),
]