from django.utils import timezone

from . import wrappers
from .models import Site, Song


class AbstractBaseCrawler():
    def __init__(self, slug, wrapper_client):
        self._site = Site.objects.get(slug=slug)
        self._slug = slug
        self._client = wrapper_client
        self._new_songs_count = 0
        self._status = 'EMPTY'

    def get_new_songs_count(self):
        return self._new_songs_count

    def _update_songs_list(self):
        songs_data = self._client.get_latest_songs()
        # today = timezone.now()
        if songs_data:
            for data in songs_data:
                song, created = Song.objects.get_or_create(
                    title=data['title'],
                    artist=data.get('artist', 'unavailable'),
                    site=self._site,
                    url=data['link']
                    )
                if created:
                    print('new song {} created'.format(data['title']))
                    self._status = 'CREATED'
                    self._new_songs_count += 1
                    song.save()

    def run(self):
        try:
            self._site.status = Site.RUNNING
            self._update_songs_list()
            self._site.last_run = timezone.now()
            self._site.save()
            self._site.status = Site.OK
        except Exception as e:
            print('Error on crawl run', e)
            self._site.status = Site.ERROR


class NaijaLoadedCrawler(AbstractBaseCrawler):
    def __init__(self, slug='naijaloaded', wrapper_client=wrappers.NaijaLoadedClient()):
        super(NaijaLoadedCrawler, self).__init__(slug, wrapper_client)


class TooXclusiveCrawler(AbstractBaseCrawler):
    def __init__(self, slug='tooxclusive', wrapper_client=wrappers.TooXclusiveClient()):
        super(TooXclusiveCrawler, self).__init__(slug, wrapper_client)


class NotJustOkClient(AbstractBaseCrawler):
    def __init__(self, slug='notjustok', wrapper_client=wrappers.NotJustOkClient()):
        super(NotJustOkClient, self).__init__(slug, wrapper_client)


if __name__ == '__main__':

    n = NaijaLoadedCrawler()
    n.run()
