from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    """Django app for SRE health checks and system status."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "monitoring"
