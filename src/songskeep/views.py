from random import shuffle

from django.views.generic import TemplateView

from services.models import Site


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        sites = list(Site.objects.filter(active=True))
        shuffle(sites)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['local_sites'] = Site.objects.get_by_category('naija')[:2]
        context['foreign_sites'] = Site.objects.get_by_category('foreign')[:2]
        context['feature_sites'] = sites[:3]

        return context
