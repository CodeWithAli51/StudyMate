from django.views.generic import TemplateView


class PracticeIndexView(TemplateView):
    template_name = 'practice/index.html'
