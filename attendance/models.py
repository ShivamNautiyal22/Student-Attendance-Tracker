from django.conf import settings
from django.db import models
from django.utils import timezone


class AttendanceRecord(models.Model):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    VERIFICATION_CHOICES = [
        (PENDING, "Pending"),
        (VERIFIED, "Verified"),
        (REJECTED, "Rejected"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    subject = models.CharField(max_length=100)
    subject_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subject_attendance_records",
    )
    date = models.DateField()
    marked_at = models.DateTimeField(default=timezone.now)
    marked_present = models.BooleanField(default=True)
    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_CHOICES, default=PENDING
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_attendance_records",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "date", "subject")
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.student.username} - {self.subject} - {self.date} - {self.verification_status}"