from django import forms

from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'display_name',
            'grade',
            'board',
            'academic_year',
            'goal',
            'preferred_daily_study_minutes',
        ]
        widgets = {
            'display_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'grade': forms.TextInput(attrs={'placeholder': 'e.g. 10'}),
            'board': forms.TextInput(attrs={'placeholder': 'e.g. Maharashtra SSC'}),
            'academic_year': forms.TextInput(attrs={'placeholder': 'e.g. 2026-27'}),
            'goal': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Score 90%+'}),
            'preferred_daily_study_minutes': forms.NumberInput(
                attrs={'min': 10, 'max': 480}
            ),
        }
