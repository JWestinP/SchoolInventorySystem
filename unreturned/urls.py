from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_unreturned_items, name="show_unreturned_items")
]