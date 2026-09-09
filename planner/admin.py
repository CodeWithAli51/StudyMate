from django.contrib import admin

from .models import StudyTask


@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'student', 'subject', 'task_type', 'status',
        'priority', 'due_date',
    )
    list_filter = ('subject', 'task_type', 'status', 'priority')
    search_fields = ('title', 'student__username', 'subject__name')
    ordering = ('due_date', '-created_at')
