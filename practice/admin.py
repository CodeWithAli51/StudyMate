from django.contrib import admin

from .models import AnswerAttempt, Question, Quiz, QuizAttempt, QuizQuestion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'subject', 'question_type', 'difficulty')
    list_filter = ('subject', 'question_type', 'difficulty')
    search_fields = ('text', 'subject__name')

    @staticmethod
    def short_text(obj):
        return obj.text[:60]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    list_filter = ('subject',)
    search_fields = ('title', 'subject__name')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question', 'order')
    list_filter = ('quiz__subject', 'quiz')
    ordering = ('quiz', 'order')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'started_at', 'completed_at')
    list_filter = ('quiz__subject', 'quiz')
    search_fields = ('quiz__title', 'student__username')
    ordering = ('-started_at',)


@admin.register(AnswerAttempt)
class AnswerAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct')
    list_filter = ('is_correct',)
