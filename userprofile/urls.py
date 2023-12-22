from django.urls import path
from . import views

urlpatterns = [
    path("userprofile", views.userprofile, name="userprofile"),
    path("admin_userprofile", views.admin_userprofile, name="admin_userprofile")
]