from django import forms

from .models import StudySession, StudyTask


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


class StudySessionFinishForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['confidence', 'reflection']
        widgets = {
            'confidence': forms.RadioSelect,
            'reflection': forms.Textarea(attrs={'rows': 3}),
        }
