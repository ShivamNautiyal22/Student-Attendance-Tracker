from django.contrib import admin
from django.urls import include, path

from users.views import home_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("users/", include("users.urls")),
    path("attendance/", include("attendance.urls")),
]
