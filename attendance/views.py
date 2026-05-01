from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from users.models import User

from .forms import AttendanceMarkForm
from .models import AttendanceRecord


@login_required
def student_dashboard_view(request):
    if not request.user.is_student():
        messages.error(request, "Only students can access this page.")
        return redirect("home")

    teacher_subjects = list(
        User.objects.filter(role=User.TEACHER)
        .exclude(subject="")
        .values_list("subject", flat=True)
        .distinct()
    )
    records = AttendanceRecord.objects.filter(student=request.user).select_related(
        "subject_teacher", "reviewed_by"
    )
    today = timezone.localdate()
    today_subjects = set(records.filter(date=today).values_list("subject", flat=True))

    if request.method == "POST":
        form = AttendanceMarkForm(request.POST, available_subjects=teacher_subjects)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            if subject in today_subjects:
                messages.info(
                    request,
                    f"You have already marked attendance for {subject} today.",
                )
                return redirect("student-dashboard")

            subject_teacher = (
                User.objects.filter(role=User.TEACHER, subject=subject).order_by("id").first()
            )
            if not subject_teacher:
                messages.error(request, f"No teacher found for subject: {subject}.")
                return redirect("student-dashboard")

            AttendanceRecord.objects.create(
                student=request.user,
                subject=subject,
                subject_teacher=subject_teacher,
                date=today,
                marked_present=True,
            )
            messages.success(
                request,
                f"Attendance marked as Present for {subject}. Pending teacher verification.",
            )
        else:
            messages.error(request, "Please select a valid subject.")
        return redirect("student-dashboard")
    else:
        form = AttendanceMarkForm(available_subjects=teacher_subjects)

    return render(
        request,
        "attendance/student_dashboard.html",
        {
            "records": records,
            "form": form,
            "teacher_subjects": teacher_subjects,
            "today_subjects": today_subjects,
        },
    )


@login_required
def teacher_dashboard_view(request):
    if not request.user.is_teacher():
        messages.error(request, "Only teachers can access this page.")
        return redirect("home")

    students = User.objects.filter(role=User.STUDENT).order_by("username")
    records = AttendanceRecord.objects.filter(subject_teacher=request.user).select_related(
        "student", "reviewed_by"
    )
    return render(
        request,
        "attendance/teacher_dashboard.html",
        {
            "students": students,
            "records": records,
        },
    )


@login_required
def update_attendance_status_view(request, record_id, status):
    if not request.user.is_teacher():
        messages.error(request, "Only teachers can perform this action.")
        return redirect("home")

    if request.method != "POST":
        return redirect("teacher-dashboard")

    if status not in [AttendanceRecord.VERIFIED, AttendanceRecord.REJECTED]:
        messages.error(request, "Invalid status update.")
        return redirect("teacher-dashboard")

    record = get_object_or_404(
        AttendanceRecord, id=record_id, subject_teacher=request.user
    )
    if record.verification_status != AttendanceRecord.PENDING:
        messages.info(request, "This record is already reviewed.")
        return redirect("teacher-dashboard")

    record.verification_status = status
    record.reviewed_by = request.user
    record.save(update_fields=["verification_status", "reviewed_by"])

    messages.success(request, f"Attendance record marked as {status}.")
    return redirect("teacher-dashboard")