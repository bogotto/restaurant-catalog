from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("dish",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "user", "created")
    list_filter = ("created",)
    search_fields = ("full_name", "phone", "address")
    inlines = (OrderItemInline,)
