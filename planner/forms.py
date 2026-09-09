from django import forms

from .models import StudyTask


class StudyTaskForm(forms.ModelForm):
    class Meta:
        model = StudyTask
        fields = [
            'title', 'subject', 'chapter', 'topic', 'task_type',
            'estimated_minutes', 'due_date', 'priority', 'status',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
