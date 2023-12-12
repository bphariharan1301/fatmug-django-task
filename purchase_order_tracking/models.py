from django.db import models
from datetime import date

# Custom models
from vendor_profile.models import Vendor

# Custom choices
from .choices import status_choices

# Create your models here.


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, to_field="vendor_code")
    order_date = models.DateField(default=date.today)
    delivery_date = models.DateField(default=date.today)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=50, choices=status_choices, default="Pending", null=True
    )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateField(default=date.today)
    acknowledgment_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            latest_po = PurchaseOrder.objects.order_by("-id").first()
            print("Inside model save: ", latest_po)
            if latest_po:
                latest_po_number = latest_po.po_number
                if latest_po_number and latest_po_number.startswith("PO-"):
                    latest_number = int(latest_po_number[3:])
                    new_number = latest_number + 1
                    self.po_number = f"PO-{str(new_number).zfill(3)}"
                else:
                    self.po_number = "PO-001"
            else:
                self.po_number = "PO-001"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.po_number + " Added Sucessfully!"
