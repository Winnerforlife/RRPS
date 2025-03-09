from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.refunds.helpers import send_notification_email
from apps.refunds.models import RefundRequest


@receiver(pre_save, sender=RefundRequest)
def refund_status_changed(sender, instance, **kwargs):
    if instance.pk:
        old_instance = RefundRequest.objects.get(pk=instance.pk)
        recipient = instance.email or instance.user.email
        if (old_instance.status != instance.status) and recipient:
            send_notification_email(
                subject="Updating the status of the return",
                message=f"The status of your refund on order #{instance.order_number} has been changed to {instance.status}",
                recipient_list=[recipient],
            )
