from django.urls import path
from . import views

urlpatterns = [
    path('members', views.members, name='members'),
    path('get_user/', views.get_user_info, name='get_user/'),
    path('get_user_history/', views.get_user_history, name='get_user_history/'),
    path('get_user_unreturned/', views.get_user_unreturned, name='get_user_unreturned/'),
]