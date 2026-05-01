from django import forms


class AttendanceMarkForm(forms.Form):
    subject = forms.ChoiceField(choices=[])

    def __init__(self, *args, available_subjects=None, **kwargs):
        super().__init__(*args, **kwargs)
        subjects = available_subjects or []
        self.fields["subject"].choices = [(subject, subject) for subject in subjects]