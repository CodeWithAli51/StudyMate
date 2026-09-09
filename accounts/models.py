from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )
    display_name = models.CharField(max_length=150, blank=True)
    grade = models.CharField(max_length=20, blank=True)
    board = models.CharField(max_length=100, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    goal = models.TextField(blank=True)
    preferred_daily_study_minutes = models.PositiveIntegerField(default=60)
    subjects = models.ManyToManyField(
        'academics.Subject',
        blank=True,
        related_name='enrolled_profiles',
    )

    def __str__(self):
        return self.display_name or self.user.username

    class Meta:
        ordering = ['user']
