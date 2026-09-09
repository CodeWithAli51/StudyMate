from django.contrib import admin

from .models import StudySession, StudyTask


@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'student', 'subject', 'task_type', 'status',
        'priority', 'due_date',
    )
    list_filter = ('subject', 'task_type', 'status', 'priority')
    search_fields = ('title', 'student__username', 'subject__name')
    ordering = ('due_date', '-created_at')


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'started_at', 'ended_at', 'confidence')
    list_filter = ('confidence', 'task__subject')
    search_fields = ('task__title', 'student__username')
    ordering = ('-started_at',)
