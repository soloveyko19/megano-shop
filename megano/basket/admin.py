from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "createdAt",
        "user",
        "fullName",
        "status",
        "totalCost",
        "deliveryType",
    )
