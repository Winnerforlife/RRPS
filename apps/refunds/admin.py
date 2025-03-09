from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.refunds.models import RefundRequest


class RefundRequestResource(resources.ModelResource):
    class Meta:
        model = RefundRequest
        fields = (
            "id",
            "user",
            "order_number",
            "order_date",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "country",
            "address",
            "postal_code",
            "city",
            "products",
            "reason",
            "bank_name",
            "account_type",
            "iban",
            "iban_verified",
            "created_at",
            "updated_at",
            "status",
        )


@admin.register(RefundRequest)
class RefundRequestAdmin(ImportExportModelAdmin):
    resource_class = RefundRequestResource
    list_display = ("id", "order_number", "status", "created_at")
    list_filter = ("status", "created_at", "country")
    search_fields = ("order_number", "email", "phone_number")
