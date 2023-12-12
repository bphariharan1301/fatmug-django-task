from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Custom Serializers
from .serializers import VendorSerializer, VendorGetSerializer

# Custom Models import
from .models import Vendor

# Create your views here.


def generate_vendor_code():
    latest_vendor = Vendor.objects.order_by("-id").first()
    if latest_vendor:
        latest_code = latest_vendor.vendor_code
        if latest_code and latest_code.startswith("VC-"):
            latest_number = int(latest_code[3:])
            new_number = latest_number + 1
            return f"VC-{str(new_number).zfill(3)}"
        else:
            return "VC-001"
    else:
        return "VC-001"


@api_view(["POST"])
def create_vendor(request):
    if request.method == "POST":
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_vendor(request):
    vendors = Vendor.objects.all()
    serializer = VendorGetSerializer(vendors, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def vendor(request, vendor_code):
    if Vendor.objects.filter(vendor_code=vendor_code).exists():
        vendor = Vendor.objects.filter(vendor_code=vendor_code).get()

        serializer = VendorGetSerializer(vendor)

        return Response(serializer.data)
    else:
        return Response("Vendor not found", status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def update_vendor(request, vendor_code):
    if request.method == "PUT":
        if Vendor.objects.filter(vendor_code=vendor_code).exists():
            vendor = Vendor.objects.filter(vendor_code=vendor_code).get()

            serializer = VendorSerializer(vendor, data=request.data)

            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data)
    else:
        return Response("Vendor not found", status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_vendor(request, vendor_code):
    if request.method == "DELETE":
        if Vendor.objects.filter(vendor_code=vendor_code).exists():
            vendor = Vendor.objects.filter(vendor_code=vendor_code).get()
            deleted_vendor = VendorGetSerializer(vendor).data
            vendor.delete()
            print("Inside if")
            context = {"message": "Vendor Deleted", "deleted_vendor": deleted_vendor}
            return Response(
                context,
                status=status.HTTP_200_OK,
            )
        else:
            return Response("Vendor not found", status=status.HTTP_404_NOT_FOUND)
