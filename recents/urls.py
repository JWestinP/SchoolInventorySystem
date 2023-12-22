from django.urls import path
from . import views

urlpatterns = [
    path('recents', views.recents, name='recents'),
    path('admin_recents', views.admin_recents, name='admin_recents'),
]