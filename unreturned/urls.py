from django.urls import path
from . import views

urlpatterns = [
    path("unreturned", views.unreturned, name="unreturned"),
    path("admin_unreturned", views.admin_unreturned, name="admin_unreturned"),
    path('return_item/<item_id>/<item_stock_id>/<borrow_form_id>', views.return_item, name="return_item"),
    path('admin_return_item/<item_id>/<item_stock_id>/<borrow_form_id>', views.admin_return_item, name="admin_return_item")
]