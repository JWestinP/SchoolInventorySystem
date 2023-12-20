from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name = 'login'),
    path('login', views.user_login, name = 'login'),
]