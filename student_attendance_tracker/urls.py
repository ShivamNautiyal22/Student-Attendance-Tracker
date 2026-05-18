from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # SRE monitoring routes (health check + status page)
    path("", include("monitoring.urls")),
    path("users/", include("users.urls")),
    path("", include("users.urls")),
    path("attendance/", include("attendance.urls")),
]
