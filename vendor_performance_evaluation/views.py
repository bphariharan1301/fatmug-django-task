from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Custom models
from vendor_profile.models import Vendor
from purchase_order_tracking.models import PurchaseOrder

# Custom Serializers
from .serializers import VendorPerformanceSerializer

# Create your views here.


@api_view(["GET"])
def specific_vendor_performance(request, vendor_code):
    if request.method == "GET":
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)

        serializer = VendorPerformanceSerializer(vendor)

        return Response(serializer.data, status=status.HTTP_200_OK)
