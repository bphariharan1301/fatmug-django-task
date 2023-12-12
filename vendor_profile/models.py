from django.db import models

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=40)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            latest_vendor = Vendor.objects.order_by("-id").first()
            if latest_vendor:
                latest_code = latest_vendor.vendor_code
                if latest_code and latest_code.startswith("VC-"):
                    latest_number = int(latest_code[3:])
                    new_number = latest_number + 1
                    self.vendor_code = f"VC-{str(new_number).zfill(3)}"
                else:
                    self.vendor_code = "VC-001"
            else:
                self.vendor_code = "VC-001"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + self.vendor_code
