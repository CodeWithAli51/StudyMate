from django.views.generic import TemplateView


class AssistantIndexView(TemplateView):
    template_name = 'assistant/index.html'
