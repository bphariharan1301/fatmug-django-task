from django.db import models
from django.utils import timezone

# Custom Models
from vendor_profile.models import Vendor

# Create your models here.

"""
  ● vendor: ForeignKey - Link to the Vendor model.
  ● date: DateTimeField - Date of the performance record.
  ● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
  ● quality_rating_avg: FloatField - Historical record of the quality rating average.
  ● average_response_time: FloatField - Historical record of the average response
  time.
  ● fulfillment_rate: FloatField - Historical record of the fulfilment rate.
"""


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, to_field="vendor_code")
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.vendor + " Added successfully"
