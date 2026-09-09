from datetime import timedelta

from django.utils import timezone

from .models import StudySession, StudyTask


def get_study_days(user):
    """Dates with at least one completed task or finished session."""
    days = set()
    completed_at_values = StudyTask.objects.filter(
        student=user,
        status=StudyTask.STATUS_COMPLETED,
        completed_at__isnull=False,
    ).values_list('completed_at', flat=True)
    for completed_at in completed_at_values:
        days.add(timezone.localdate(completed_at))
    ended_at_values = StudySession.objects.filter(
        student=user, ended_at__isnull=False
    ).values_list('ended_at', flat=True)
    for ended_at in ended_at_values:
        days.add(timezone.localdate(ended_at))
    return days


def get_streaks(user):
    """Current and longest study streaks, derived from source records."""
    days = get_study_days(user)
    if not days:
        return {'current': 0, 'longest': 0}
    ordered = sorted(days)
    longest = run = 1
    for previous, day in zip(ordered, ordered[1:]):
        if day - previous == timedelta(days=1):
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    today = timezone.localdate()
    start = today if today in days else today - timedelta(days=1)
    current = 0
    while start in days:
        current += 1
        start -= timedelta(days=1)
    return {'current': current, 'longest': longest}
