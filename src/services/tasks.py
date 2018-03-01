from django.conf import settings

from celery import shared_task
from celery.task import task
from celery.utils.log import get_task_logger
from services.models import Subscription
from services import crawlers
from songskeep.utils import Emailer

logger = get_task_logger(__name__)


@task(name='run_crawls_for_sites_task')
def run_crawls_for_sites_task():
    site_crawlers = [crawlers.TooXclusiveCrawler(), crawlers.NaijaLoadedCrawler()]
    count = 0
    for c in site_crawlers:
        c.run()
        # logger.info('results', results['num'])
        count += c.get_new_songs_count()

    logger.info('Crawled sites. {} new songs'.format(str(count)))
    if count > 0:
        subscribers = Subscription.objects.filter(active=True)
        if len(subscribers) < 1:
            logger.info('There are no subscribers. No emails sent.')
            return

        email_dets_kwargs = {
            'recipients': [x.email for x in subscribers],
            'type': 'UPDATE'
        }
        em = Emailer(**email_dets_kwargs)
        em.send_email()
        logger.info('Sent email to subscribers')


@shared_task
def send_email_on_subscription_task(email):
    email_dets_kwargs = {
        'recipients': [email],
        'type': 'WELCOME'
    }
    em = Emailer(**email_dets_kwargs)
    em.send_email()
