from django import forms


class AttendanceMarkForm(forms.Form):
    enrollment = forms.ChoiceField(choices=[])

    def __init__(self, *args, available_enrollments=None, **kwargs):
        super().__init__(*args, **kwargs)
        enrollments = available_enrollments or []
        self.fields["enrollment"].choices = [
            (str(enrollment.id), f"{enrollment.teacher.subject} ({enrollment.teacher.username})")
            for enrollment in enrollments
        ]