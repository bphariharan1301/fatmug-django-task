from rest_framework import serializers
from datetime import datetime, timedelta

# Custom Models
from .models import PurchaseOrder
from vendor_profile.models import Vendor


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = [
            "vendor",
            "items",
            "quantity",
            "order_date",
            "issue_date",
            "delivery_date",
            "status",
            "quality_rating",
            "acknowledgment_date",
        ]

    def create(self, validated_data):
        # No changes to the create method from the previous example
        order_date = validated_data.get("order_date") or datetime.today().date()
        issue_date = validated_data.get("issue_date") or order_date
        delivery_date = validated_data.get("delivery_date") or order_date + timedelta(
            days=3
        )

        print(order_date, issue_date, delivery_date)

        purchase_order = PurchaseOrder.objects.create(
            vendor=validated_data["vendor"],
            items=validated_data["items"],
            quantity=validated_data["quantity"],
            order_date=order_date,
            issue_date=issue_date,
            delivery_date=delivery_date,
        )

        purchase_order.save()
        return purchase_order
