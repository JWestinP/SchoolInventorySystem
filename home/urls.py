from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('guest_home', views.guest_home, name='guest_home'),
    path('recents', views.recents, name='recents'),
    path('unreturned', views.unreturned, name='unreturned'),
    path('notification', views.notification, name='notification'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('members', views.members, name='members'),
    path('admin_recents', views.admin_recents, name='admin_recents'),
    path('admin_unreturned', views.admin_unreturned, name='admin_unreturned'),
    path('admin_userprofile', views.admin_userprofile, name='admin_userprofile'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('guest_home', views.guest_home, name='guest_home'),
]