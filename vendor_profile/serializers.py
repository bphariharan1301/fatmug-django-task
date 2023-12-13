from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name", "contact_details", "address"]
        read_only_fields = ["vendor_code"]


class VendorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
