from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.models import StudentProfile
from planner.models import StudySession, StudyTask
from planner.views import get_today_plan


class LandingView(TemplateView):
    template_name = 'dashboard/landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = StudentProfile.objects.filter(user=user).first()
        name = profile.display_name if profile and profile.display_name else user.username
        hour = timezone.localtime().hour
        if hour < 12:
            greeting = 'Good morning'
        elif hour < 17:
            greeting = 'Good afternoon'
        else:
            greeting = 'Good evening'
        plan = get_today_plan(user)
        recent_completions = StudyTask.objects.filter(
            student=user, status=StudyTask.STATUS_COMPLETED
        ).select_related('subject').order_by('-completed_at')[:5]
        recent_sessions = StudySession.objects.filter(
            student=user, ended_at__isnull=False
        ).select_related('task', 'task__subject').order_by('-started_at')[:5]
        context.update({
            'greeting': greeting,
            'name': name,
            'plan': plan,
            'recent_completions': recent_completions,
            'recent_sessions': recent_sessions,
        })
        return context
