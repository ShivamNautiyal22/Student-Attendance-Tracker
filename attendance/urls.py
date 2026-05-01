from django.urls import path

from .views import (
    remove_student_from_class_view,
    student_dashboard_view,
    teacher_dashboard_view,
    update_student_comment_view,
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
    path(
        "teacher/class/<int:enrollment_id>/remove/",
        remove_student_from_class_view,
        name="remove-student-from-class",
    ),
    path(
        "teacher/class/<int:enrollment_id>/comment/",
        update_student_comment_view,
        name="update-student-comment",
    ),
]