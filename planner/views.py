from django.views.generic import TemplateView


class PlannerIndexView(TemplateView):
    template_name = 'planner/index.html'
