from django.urls import path

from apps.refunds.views import CreateRefundRequestView, RefundRequestDetailView, RefundRequestListView


urlpatterns = [
    path('create/', CreateRefundRequestView.as_view(), name='create_refund'),
    path('', RefundRequestListView.as_view(), name='refund_list'),
    path('<int:pk>/', RefundRequestDetailView.as_view(), name='refund_detail'),
]
