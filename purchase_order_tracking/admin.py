from django.contrib import admin

# Custom models
from .models import PurchaseOrder

# Register your models here.
admin.site.register(PurchaseOrder)
