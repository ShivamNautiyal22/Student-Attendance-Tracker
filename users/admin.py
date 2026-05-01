from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import ClassEnrollment, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Role Data", {"fields": ("role", "subject", "bio")}),
    )
    list_display = ("username", "email", "role", "subject", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("teacher", "student", "is_active", "updated_at")
    list_filter = ("is_active", "teacher")
    search_fields = ("teacher__username", "student__username")
