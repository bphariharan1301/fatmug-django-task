from django.contrib import admin

# Custom models
from .models import HistoricalPerformance

# Register your models here.
admin.site.register(HistoricalPerformance)
