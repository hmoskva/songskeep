from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from django.views import generic
from django.views.generic.base import TemplateResponseMixin

from .models import Site, Song, Subscription
from .forms import SubscriptionForm
from .tasks import send_email_on_subscription_task


class SiteListView(generic.ListView):
    template_name = 'services/service_index.html'
    model = Site
    context_object_name = 'sites'

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        if category:
            sites = Site.objects.filter(category=category, active=True)
            return sites
        return []


class SongListView(TemplateResponseMixin, generic.View):
    # template_name = 'services/songs_list.html'

    def get(self, *args, **kwargs):
        data = dict()
        site = get_object_or_404(Site, slug=kwargs.get('slug'))
        data['site_info'] = {'title': site.name, 'propp': site.props,
                             'a_link': site.get_archive_url()}
        data['songs_html_list'] = render_to_string(
            'services/includes/songs_list.html',
            {'songs': site.songs.all()[:5]},
            self.request
        )
        return JsonResponse(data)


# class SubscriptionCreateView(generic.CreateView):
#     model = Subscription
#     form_class = SubscriptionForm
#
#     def get_form_kwargs(self):
#         kwargs = super(SubscriptionCreateView, self).get_form_kwargs()
#         kwargs['category'] = self.request.GET.get('category', 'naija')


def subscribe(request):
    data = dict()
    if request.method == 'POST':
        email = request.POST.get('email', None)
        action = request.POST.get('action', None)
        print(email,'-->',action)
        if email is not None:
            if action == 'subscribe':
                sub, created = Subscription.objects.get_or_create(email=email)
                if created:
                    sub.save()
                    send_email_on_subscription_task.delay(email)
                    data['OK_message'] = 'You have successfully subscribed for updates.' \
                                      'You will get email notifications as new songs are posted.'
                    data['toast_color'] = 'info'
                else:
                    data['OK_message'] = 'You have already been subscribed to this service'
                    data['toast_color'] = 'danger'
            else:
                try:
                    sub = Subscription.objects.filter(email=email)
                    if sub.exists() and len(sub) == 1:
                        sub.first().active = False
                        data['DEL_message'] = 'You have successfully unsubscribed from this service :('
                except Subscription.DoesNotExist:
                    raise ReferenceError('this shit doesnt exist')

        else:
            data['ERR_message'] = 'Not subscribed'
        return JsonResponse(data)

    return render(request, '404.html')


def songs_archive(request, slug):
    site = get_object_or_404(Site, slug=slug)
    page = request.GET.get('page', 1)
    paginator = Paginator(site.songs.all(), 10)
    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        songs = paginator.page(1)
    except EmptyPage:
        songs = paginator.page(paginator.num_pages)
    context = {'site': site, 'songs': songs}
    return render(request, 'services/archive.html', context)


def fetch_ajax_sites_by_category(request):
    data = {}
    category = request.GET.get('category', None)
    print(category)
    if category is not None:
        sites = Site.objects.filter(category=category)
        data['status'] = 'OK'
        data['sites'] = [
            {'name': x.name, 'slug': x.slug} for x in sites
        ]
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)



