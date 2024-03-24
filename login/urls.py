from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name = 'login'),
    path('login', views.user_login, name = 'login'),
    path('logout', views.user_logout, name = 'logout'),
    path('guest_login', views.guest_login, name='guest_login'),
    path("reset_password", views.password_reset_request, name="reset_password")
]