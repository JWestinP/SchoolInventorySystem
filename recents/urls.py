from django.urls import path
from . import views

urlpatterns = [
    path('recents', views.recents, name='recents'),
    path('admin_recents', views.admin_recents, name='admin_recents'),
    path('admin_search_recents', views.admin_search_recents, name='admin_search_recents'),
    path('faculty_search_recents', views.faculty_search_recents, name='faculty_search_recents'),
]