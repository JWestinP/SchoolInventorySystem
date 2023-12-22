from django.urls import path
from . import views

urlpatterns = [
    path("show_unreturned_items", views.show_unreturned_items, name="show_unreturned_items"),
    path("admin_unreturned", views.admin_unreturned, name="admin_unreturned")
]