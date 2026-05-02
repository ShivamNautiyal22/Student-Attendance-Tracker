from django import forms


class AttendanceMarkForm(forms.Form):
    teacher = forms.ChoiceField(choices=[])

    def __init__(self, *args, available_teachers=None, **kwargs):
        super().__init__(*args, **kwargs)
        teachers = available_teachers or []
        self.fields["teacher"].choices = [
            (str(teacher.id), f"{teacher.subject} ({teacher.username})")
            for teacher in teachers
        ]