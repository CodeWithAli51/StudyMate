from django.views.generic import TemplateView


class AcademicsIndexView(TemplateView):
    template_name = 'academics/index.html'
