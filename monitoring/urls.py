"""
URL routes for SRE monitoring (health check + status page).
"""

from django.urls import path

from . import views

urlpatterns = [
    # JSON health check — used by Docker and DevOps scripts
    path("health/", views.health_check, name="health-check"),
    # Visual status page for demos and quick troubleshooting
    path("status/", views.system_status, name="system-status"),
]
