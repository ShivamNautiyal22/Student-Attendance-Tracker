from django.urls import path

from .views import (
    student_dashboard_view,
    teacher_dashboard_view,
    update_attendance_status_view,
)


urlpatterns = [
    path("student/", student_dashboard_view, name="student-dashboard"),
    path("teacher/", teacher_dashboard_view, name="teacher-dashboard"),
    path(
        "teacher/records/<int:record_id>/<str:status>/",
        update_attendance_status_view,
        name="attendance-status-update",
    ),
]