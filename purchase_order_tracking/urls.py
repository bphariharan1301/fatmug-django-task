from django.urls import path, include
from . import views

"""
● POST /api/purchase_orders/: Create a purchase order.
● GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.
● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
● PUT /api/purchase_orders/{po_id}/: Update a purchase order.
● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
"""

urlpatterns = [
    path("purchase_orders", view=views.purchase_orders, name="purchase-orders"),
    path(
        "purchase_orders/<str:po_number>",
        view=views.specific_purchase_orders,
        name="purchase-orders",
    ),
]
