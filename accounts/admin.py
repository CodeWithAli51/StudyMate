from django.contrib import admin

from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'grade', 'board')
    search_fields = ('user__username', 'display_name', 'grade', 'board')
