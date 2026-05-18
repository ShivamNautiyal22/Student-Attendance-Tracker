"""
SRE views: health check (JSON API) and system status page (HTML).
"""

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET

from .utils import get_recent_log_lines, is_database_connected


@require_GET
def health_check(request):
    """
    Simple health endpoint for load balancers, Docker, and manual checks.

    Example: GET http://localhost:8000/health/
    Returns JSON with status "healthy" or "unhealthy".
    """
    db_ok = is_database_connected()

    data = {
        "status": "healthy" if db_ok else "unhealthy",
        "service": "Student Attendance Tracker",
        "database": "connected" if db_ok else "disconnected",
        "timestamp": timezone.now().isoformat(),
    }

    # HTTP 503 tells monitoring tools the service is down
    http_status = 200 if db_ok else 503
    return JsonResponse(data, status=http_status)


@require_GET
def system_status(request):
    """
    Human-friendly status page at /status/

    Shows app health, database, current time, and recent log lines.
    """
    db_ok = is_database_connected()
    app_ok = db_ok  # For this project, "app is up" if DB works

    context = {
        "app_status": "Running" if app_ok else "Problem detected",
        "app_healthy": app_ok,
        "database_status": "Connected" if db_ok else "Not connected",
        "database_healthy": db_ok,
        "current_time": timezone.now(),
        "recent_logs": get_recent_log_lines(limit=8),
    }
    return render(request, "monitoring/status.html", context)
