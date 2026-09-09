from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class StudyTask(models.Model):
    TASK_LEARN = 'learn'
    TASK_PRACTICE = 'practice'
    TASK_REVISE = 'revise'
    TASK_TEST = 'test'
    TASK_HOMEWORK = 'homework'
    TASK_READING = 'reading'
    TASK_DOUBT = 'doubt'
    TASK_TYPE_CHOICES = [
        (TASK_LEARN, 'Learn'),
        (TASK_PRACTICE, 'Practice'),
        (TASK_REVISE, 'Revise'),
        (TASK_TEST, 'Test'),
        (TASK_HOMEWORK, 'Homework'),
        (TASK_READING, 'Reading'),
        (TASK_DOUBT, 'Doubt'),
    ]

    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_TODO, 'Todo'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_tasks',
    )
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(
        'academics.Subject',
        on_delete=models.CASCADE,
        related_name='study_tasks',
    )
    chapter = models.ForeignKey(
        'academics.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_tasks',
    )
    topic = models.ForeignKey(
        'academics.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_tasks',
    )
    task_type = models.CharField(
        max_length=20, choices=TASK_TYPE_CHOICES, default=TASK_LEARN
    )
    estimated_minutes = models.PositiveIntegerField(
        default=30, validators=[MinValueValidator(1)]
    )
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.chapter and self.chapter.subject_id != self.subject_id:
            raise ValidationError(
                {'chapter': 'Chapter must belong to the selected subject.'}
            )
        if self.topic:
            if self.chapter and self.topic.chapter_id != self.chapter.pk:
                raise ValidationError(
                    {'topic': 'Topic must belong to the selected chapter.'}
                )
            if self.topic.chapter.subject_id != self.subject_id:
                raise ValidationError(
                    {'topic': 'Topic must belong to the selected subject.'}
                )
