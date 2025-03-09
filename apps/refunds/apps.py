from django.apps import AppConfig


class RefundsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.refunds"

    def ready(self):
        import apps.refunds.signals
