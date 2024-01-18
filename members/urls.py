from django.urls import path
from . import views

urlpatterns = [
    path('members', views.members, name='members'),
    path('get_user/', views.get_user_info, name='get_user/'),
]