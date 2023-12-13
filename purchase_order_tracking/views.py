from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Avg, F, ExpressionWrapper, FloatField

# Serializer imports
from .serializers import CreatePurchaseOrderSerializer, PurchaseOrderSerializer
from vendor_profile.serializers import VendorGetSerializer

# Custom Models
from .models import PurchaseOrder
from vendor_profile.models import Vendor
from vendor_performance_evaluation.models import HistoricalPerformance


# Create your views here.


@api_view(["POST", "GET"])
def purchase_orders(request):
    if request.method == "POST":
        serializer = CreatePurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Set default values
            order_date = (
                serializer.validated_data.get("order_date") or datetime.today().date()
            )
            issue_date = serializer.validated_data.get("issue_date") or order_date
            delivery_date = serializer.validated_data.get(
                "delivery_date"
            ) or order_date + timedelta(days=3)

            # Create PurchaseOrder instance
            purchase_order = PurchaseOrder.objects.create(
                vendor=serializer.validated_data["vendor"],
                items=serializer.validated_data["items"],
                quantity=serializer.validated_data["quantity"],
                order_date=order_date,
                issue_date=issue_date,
                delivery_date=delivery_date,
            )

            purchase_order.save()

            return Response(
                {
                    "message": "Purchase Order created successfully!",
                    "po_number": purchase_order.po_number,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        vendor_code = request.query_params.get("vendor", None)
        print("Vendor_code: ", vendor_code)
        if vendor_code:
            print("Inside If")
            if PurchaseOrder.objects.filter(vendor_id=vendor_code).exists():
                purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_code)
                print("Purchase Orders: ", purchase_orders)
            else:
                return Response(
                    f"Purchase for the vendor with id {vendor_code} not found",
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            print("Inside Else")
            purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def specific_purchase_orders(request, po_number):
    print("Inside fun()")
    purchase_order = get_object_or_404(PurchaseOrder, po_number=po_number)
    vendor = purchase_order.vendor

    if request.method == "GET":
        if purchase_order:
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        if purchase_order:
            serializer = CreatePurchaseOrderSerializer(
                purchase_order, data=request.data
            )

            if request.data["status"] == "Completed":
                delivery_date = datetime.today()

                # Update on-time delivery rate
                completed_pos_count = PurchaseOrder.objects.filter(
                    vendor=vendor,
                    status="Completed",
                    delivery_date__lte=delivery_date,
                ).count()

                total_completed_pos_count = PurchaseOrder.objects.filter(
                    vendor=vendor, status="Completed"
                ).count()

                if total_completed_pos_count != 0:
                    on_time_delivery_rate = (
                        completed_pos_count / total_completed_pos_count
                    )
                    vendor.on_time_delivery_rate = on_time_delivery_rate

                # Update quality rating avg
                if request.data.get("quality_rating"):
                    average_quality_rating = PurchaseOrder.objects.filter(
                        vendor=vendor, status="Completed"
                    ).aggregate(avg_quality=Avg("quality_rating"))
                    print("average_quality_rating: ", average_quality_rating)
                    vendor.quality_rating_avg = (
                        average_quality_rating["avg_quality"]
                    ) or 0.0
                vendor_history = HistoricalPerformance.objects.create(
                    vendor=vendor,
                    date=datetime.today(),
                    on_time_delivery_rate=on_time_delivery_rate,
                    quality_rating_avg=average_quality_rating["avg_quality"],
                )
                vendor.save()
                vendor_history.save()

            # fulfillment rate
            if request.data.get("status"):
                if purchase_order.status != request.data["status"]:
                    vendor_completed_pos_count = PurchaseOrder.objects.filter(
                        vendor=vendor,
                        status="Completed",
                        delivery_date__lte=delivery_date,
                    ).count()

                    total_pos_issued_count = PurchaseOrder.objects.filter(
                        vendor=vendor,
                    ).count()

                    fulfillment_rate = (
                        vendor_completed_pos_count / total_pos_issued_count
                    )
                    vendor.fulfillment_rate = fulfillment_rate
                    vendor.save()
                    vendor_history = HistoricalPerformance.objects.create(
                        vendor=vendor.vendor_code,
                        date=datetime.today(),
                        on_time_delivery_rate=on_time_delivery_rate,
                        quality_rating_avg=average_quality_rating["avg_quality"],
                        fulfillment_rate=fulfillment_rate,
                    )

                    vendor_history.save()

            print("After request if")
            if serializer.is_valid():
                print("Inside serializer valid()")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        purchase_order.delete()
        return Response("Deleted successfully!", status=status.HTTP_200_OK)


@api_view(["POST"])
def acknowledge_purchase_order(request, po_number):
    purchase_order = get_object_or_404(PurchaseOrder, po_number=po_number)

    # Set acknowledgment_date to today's date
    purchase_order.acknowledgment_date = datetime.today().date()

    # Save the purchase_order
    purchase_order.save()

    # Get the vendor for the purchase_order
    vendor = purchase_order.vendor

    # Calculate time difference for each PO
    time_differences = Avg(
        PurchaseOrder.objects.all()
        .annotate(time_difference=F("acknowledgment_date") - F("issue_date"))
        .values_list("time_difference", flat=True)
    )

    print("time diff: ", time_differences)

    # Calculate average time difference for all POs of the vendor
    average_response_time = PurchaseOrder.objects.filter(vendor=vendor).aggregate(
        avg_time_difference=ExpressionWrapper(
            Avg(F("acknowledgment_date") - F("issue_date")), output_field=FloatField()
        )
    )["avg_time_difference"]

    # Additional logic or response as needed

    vendor.average_response_time = average_response_time
    print(type(average_response_time))
    print(average_response_time)

    serializer = VendorGetSerializer(instance=vendor)
    vendor.save()

    # Return a response, you may modify this as per your needs
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )
