from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm
from .models import ClassEnrollment, User


def home_view(request):
    return JsonResponse(
        {
            "message": "Student Attendance Tracker Backend",
            "authenticated": request.user.is_authenticated,
            "user_role": request.user.role if request.user.is_authenticated else None,
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"error": "Already authenticated."}, status=400)

    form = RegisterForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    user = form.save()
    login(request, user)
    return JsonResponse(
        {
            "message": "Account created successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "subject": user.subject,
                "bio": user.bio,
            },
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    username = (request.POST.get("username") or "").strip()
    password = request.POST.get("password") or ""
    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"error": "Invalid credentials."}, status=400)
    login(request, user)
    return JsonResponse({"message": "Logged in successfully."})


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully."})


@login_required
def profile_view(request):
    current_user = request.user
    enrollments = []
    if current_user.is_teacher():
        enrollments = (
            ClassEnrollment.objects.filter(teacher=current_user, is_active=True)
            .select_related("student")
            .order_by("student__username")
        )
    elif current_user.is_student():
        enrollments = (
            ClassEnrollment.objects.filter(student=current_user, is_active=True)
            .select_related("teacher")
            .order_by("teacher__username")
        )
    elif current_user.is_admin():
        enrollments = (
            ClassEnrollment.objects.filter(is_active=True)
            .select_related("teacher", "student")
            .order_by("teacher__username", "student__username")
        )

    enrollment_data = []
    for enrollment in enrollments:
        enrollment_data.append(
            {
                "id": enrollment.id,
                "teacher": enrollment.teacher.username,
                "student": enrollment.student.username,
                "progress_comment": enrollment.progress_comment,
                "is_active": enrollment.is_active,
            }
        )

    return JsonResponse(
        {
            "profile": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "role": current_user.role,
                "subject": current_user.subject,
                "bio": current_user.bio,
            },
            "enrollments": enrollment_data,
            "users_count": User.objects.count() if current_user.is_admin() else None,
        }
    )
