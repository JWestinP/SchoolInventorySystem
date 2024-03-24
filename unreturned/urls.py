from django.urls import path
from . import views

urlpatterns = [
    path("unreturned", views.unreturned, name="unreturned"),
    path("admin_unreturned", views.admin_unreturned, name="admin_unreturned"),
    path('admin_search_unreturned', views.admin_search_unreturned, name='admin_search_unreturned'),
    path('faculty_search_unreturned', views.faculty_search_unreturned, name='faculty_search_unreturned'),
    path('get_return_form/', views.get_return_form, name='get_return_form'),
    path('save_return_form/', views.save_return_form, name='save_return_form'),
    path('get_borrow_info/', views.get_borrow_info, name='get_borrow_info'),
]