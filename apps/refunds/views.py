from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.refunds.forms import RefundRequestForm
from apps.refunds.helpers import validate_iban
from apps.refunds.models import RefundRequest


class CreateRefundRequestView(LoginRequiredMixin, CreateView):
    model = RefundRequest
    form_class = RefundRequestForm
    template_name = "refunds/create.html"
    success_url = reverse_lazy("refund_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        result = validate_iban(self.object.iban)
        self.object.iban_verified = result.get("valid", False)
        self.object.save(update_fields=["iban_verified"])
        return response


class RefundRequestListView(LoginRequiredMixin, ListView):
    model = RefundRequest
    template_name = "refunds/list.html"
    context_object_name = "refund_requests"

    def get_queryset(self):
        return RefundRequest.objects.filter(user=self.request.user)


class RefundRequestDetailView(LoginRequiredMixin, DetailView):
    model = RefundRequest
    template_name = "refunds/detail.html"
    context_object_name = "refund_request"

    def get_queryset(self):
        return RefundRequest.objects.filter(user=self.request.user)


class ValidateIBANAPIView(APIView):
    def get(self, request, format=None):
        iban = request.query_params.get("iban", "").strip()
        if not iban:
            return Response(
                {"error": "IBAN not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        result = validate_iban(iban)
        if result.get("valid"):
            return Response({"valid": True})
        else:
            return Response(
                {"valid": False, "reason": result.get("reason", "Invalid IBAN.")}
            )
