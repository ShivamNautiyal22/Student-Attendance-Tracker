from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "subject_teacher", "date", "verification_status", "reviewed_by")
    list_filter = ("verification_status", "subject", "date")
    search_fields = ("student__username", "subject", "subject_teacher__username")