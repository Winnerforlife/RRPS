from django.contrib import admin

from apps.refunds.models import RefundRequest


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "order_number", "status", "created_at")
    list_filter = ("status", "created_at", "country")
    search_fields = ("order_number", "email", "phone_number")
