from django.views.generic import TemplateView


class RevisionIndexView(TemplateView):
    template_name = 'revision/index.html'
