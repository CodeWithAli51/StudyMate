from django.shortcuts import redirect
from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = 'dashboard/landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)


class DashboardHomeView(TemplateView):
    template_name = 'dashboard/home.html'
