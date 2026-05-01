from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    subject = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def is_student(self):
        return self.role == self.STUDENT

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class ClassEnrollment(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="class_enrollments",
        limit_choices_to={"role": User.TEACHER},
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrolled_classes",
        limit_choices_to={"role": User.STUDENT},
    )
    progress_comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("teacher", "student")
        ordering = ["teacher__username", "student__username"]

    def __str__(self):
        return f"{self.student.username} in {self.teacher.username}'s class"
