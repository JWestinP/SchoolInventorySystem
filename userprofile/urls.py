from django.urls import path
from . import views

urlpatterns = [
    path("userprofile", views.userprofile, name="userprofile"),
    path("editprofile", views.editprofile, name="editprofile"),
    path("editprofileadmin", views.editprofile_admin, name="editprofileadmin"),
    path("admin_userprofile", views.admin_userprofile, name="admin_userprofile"),
]