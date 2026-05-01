from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from users.models import ClassEnrollment

from .forms import AttendanceMarkForm
from .models import AttendanceRecord


@login_required
@require_http_methods(["GET", "POST"])
@csrf_exempt
def student_dashboard_view(request):
    if not request.user.is_student():
        return JsonResponse({"error": "Only students can access this endpoint."}, status=403)

    enrollments = list(
        ClassEnrollment.objects.filter(student=request.user, is_active=True)
        .select_related("teacher")
        .exclude(teacher__subject="")
    )
    records = AttendanceRecord.objects.filter(student=request.user).select_related(
        "subject_teacher", "reviewed_by"
    )
    today = timezone.localdate()
    today_subjects = set(records.filter(date=today).values_list("subject", flat=True))

    if request.method == "POST":
        form = AttendanceMarkForm(request.POST, available_enrollments=enrollments)
        if form.is_valid():
            enrollment_id = int(form.cleaned_data["enrollment"])
            enrollment = next((item for item in enrollments if item.id == enrollment_id), None)
            if not enrollment:
                return JsonResponse({"error": "Invalid class selection."}, status=400)
            subject = enrollment.teacher.subject
            if subject in today_subjects:
                return JsonResponse(
                    {"message": f"You have already marked attendance for {subject} today."},
                    status=200,
                )

            record = AttendanceRecord.objects.create(
                student=request.user,
                subject=subject,
                subject_teacher=enrollment.teacher,
                date=today,
                marked_at=timezone.now(),
                marked_present=True,
            )
            return JsonResponse(
                {
                    "message": f"Attendance marked as Present for {subject}. Pending teacher verification.",
                    "record_id": record.id,
                },
                status=201,
            )
        return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse(
        {
            "available_enrollments": [
                {
                    "enrollment_id": enrollment.id,
                    "teacher_id": enrollment.teacher.id,
                    "teacher_username": enrollment.teacher.username,
                    "subject": enrollment.teacher.subject,
                }
                for enrollment in enrollments
            ],
            "records": [
                {
                    "id": record.id,
                    "subject": record.subject,
                    "teacher": record.subject_teacher.username,
                    "date": record.date.isoformat(),
                    "marked_at": record.marked_at.isoformat(),
                    "verification_status": record.verification_status,
                    "reviewed_by": record.reviewed_by.username if record.reviewed_by else None,
                }
                for record in records
            ],
        }
    )


@login_required
@require_http_methods(["GET"])
def teacher_dashboard_view(request):
    if not request.user.is_teacher():
        return JsonResponse({"error": "Only teachers can access this endpoint."}, status=403)

    students = (
        ClassEnrollment.objects.filter(teacher=request.user, is_active=True)
        .select_related("student")
        .order_by("student__username")
    )
    records = AttendanceRecord.objects.filter(subject_teacher=request.user).select_related(
        "student", "reviewed_by"
    )
    return JsonResponse(
        {
            "students": [
                {
                    "enrollment_id": enrollment.id,
                    "student_id": enrollment.student.id,
                    "student_username": enrollment.student.username,
                    "progress_comment": enrollment.progress_comment,
                }
                for enrollment in students
            ],
            "records": [
                {
                    "record_id": record.id,
                    "student": record.student.username,
                    "subject": record.subject,
                    "date": record.date.isoformat(),
                    "marked_at": record.marked_at.isoformat(),
                    "verification_status": record.verification_status,
                    "reviewed_by": record.reviewed_by.username if record.reviewed_by else None,
                }
                for record in records
            ],
        }
    )


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_attendance_status_view(request, record_id, status):
    if not request.user.is_teacher():
        return JsonResponse({"error": "Only teachers can perform this action."}, status=403)

    if status not in [AttendanceRecord.VERIFIED, AttendanceRecord.REJECTED]:
        return JsonResponse({"error": "Invalid status update."}, status=400)

    record = get_object_or_404(
        AttendanceRecord, id=record_id, subject_teacher=request.user
    )
    if record.verification_status != AttendanceRecord.PENDING:
        return JsonResponse({"message": "This record is already reviewed."}, status=200)

    record.verification_status = status
    record.reviewed_by = request.user
    record.save(update_fields=["verification_status", "reviewed_by"])

    return JsonResponse({"message": f"Attendance record marked as {status}."})


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def remove_student_from_class_view(request, enrollment_id):
    if not request.user.is_teacher():
        return JsonResponse({"error": "Only teachers can perform this action."}, status=403)

    enrollment = get_object_or_404(
        ClassEnrollment, id=enrollment_id, teacher=request.user, is_active=True
    )
    enrollment.is_active = False
    enrollment.save(update_fields=["is_active", "updated_at"])
    return JsonResponse({"message": f"{enrollment.student.username} was removed from your class."})


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_student_comment_view(request, enrollment_id):
    if not request.user.is_teacher():
        return JsonResponse({"error": "Only teachers can perform this action."}, status=403)

    enrollment = get_object_or_404(
        ClassEnrollment, id=enrollment_id, teacher=request.user, is_active=True
    )
    enrollment.progress_comment = (request.POST.get("progress_comment") or "").strip()
    enrollment.save(update_fields=["progress_comment", "updated_at"])
    return JsonResponse({"message": f"Progress comment updated for {enrollment.student.username}."})