from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "vendors/<str:vendor_code>/performance",
        view=views.specific_vendor_performance,
        name="specific-vendor-performance",
    ),
]
