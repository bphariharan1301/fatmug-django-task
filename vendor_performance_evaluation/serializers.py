from rest_framework import serializers
from vendor_profile.models import Vendor
from purchase_order_tracking.models import PurchaseOrder


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "vendor_code",
            "name",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]
