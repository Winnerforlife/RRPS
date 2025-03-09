from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView

from apps.refunds.forms import RefundRequestForm
from apps.refunds.models import RefundRequest


class CreateRefundRequestView(LoginRequiredMixin, CreateView):
    model = RefundRequest
    form_class = RefundRequestForm
    template_name = "refunds/create.html"
    success_url = reverse_lazy("refund_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
