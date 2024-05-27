from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('get_items/', views.get_items, name='get_items'),
    path('get_category/', views.get_category, name='get_category'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('guest_home', views.guest_home, name='guest_home'),
    path('item_inventory/', views.get_item_inventory, name='get_item_inventory'),
    path('get_borrow_form/', views.get_borrow_form, name='get_borrow_form'),
    path('get_guest_borrow_form/', views.get_guest_borrow_form, name='get_guest_borrow_form'),
    path('get_item_form/', views.get_item_form, name='get_item_form'),
    path('get_stock_form/', views.get_stock_form, name='get_stock_form'),
    path('get_category_form/', views.get_category_form, name='get_category_form'),
    path('save_borrow_form/', views.save_borrow_form, name='save_borrow_form'),
    path('guest_save_borrow_form/', views.guest_save_borrow_form, name='guest_save_borrow_form'),
    path('save_item_form/', views.save_item_form, name='save_item_form'),
    path('save_stock_form/', views.save_stock_form, name='save_stock_form'),
    path('save_category_form/', views.save_category_form, name='save_category_form'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('delete_category/', views.delete_category, name='delete_category'),
    path('search_items/', views.search_items, name='search_items'),
    path('search_items_admin/', views.search_items_admin, name='search_items_admin'),
    path('search_items_guest/', views.search_items_guest, name='search_items_guest'),
]