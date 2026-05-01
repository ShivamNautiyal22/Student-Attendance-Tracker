from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "role", "subject", "bio", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        subject = (cleaned_data.get("subject") or "").strip()
        if role == User.TEACHER and not subject:
            self.add_error("subject", "Teachers must have a subject.")
        if role != User.TEACHER:
            cleaned_data["subject"] = ""
        return cleaned_data
