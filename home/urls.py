from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('guest_home', views.guest_home, name='guest_home'),
]