from django.urls import path
from . import views

urlpatterns = [
    path("unreturned", views.unreturned, name="unreturned"),
    path("admin_unreturned", views.admin_unreturned, name="admin_unreturned"),
    path('return_item/<item_id>', views.return_item, name="return_item")
]