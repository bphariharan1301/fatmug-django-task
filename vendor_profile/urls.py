from django.urls import path, include
from . import views

urlpatterns = [
    path("", view=views.list_vendor, name="list-vendor"),
    path("create-vendor", view=views.create_vendor, name="create-vendor"),
    path("vendor/<str:vendor_code>", view=views.vendor, name="vendor"),
    path(
        "update-vendor/<str:vendor_code>",
        view=views.update_vendor,
        name="update-vendor",
    ),
    path(
        "delete-vendor/<str:vendor_code>",
        view=views.delete_vendor,
        name="delete-vendor",
    ),
]
