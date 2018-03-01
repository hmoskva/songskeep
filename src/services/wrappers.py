import json
import re
import requests

from bs4 import BeautifulSoup


class AbstractBaseClient():
    def __init__(self, url):
        self._page = requests.get(url)
        self._soup = BeautifulSoup(self._page.text, 'html.parser')
        self._body = self._soup.body

    def get_latest_songs(self):
        return NotImplemented


class NaijaLoadedClient(AbstractBaseClient):
    def __init__(self):
        super(NaijaLoadedClient, self).__init__(url='http://www.naijaloaded.com.ng')

    def get_latest_songs(self):
        new_songs_wrapper = self._body.find_all(class_='trending-single')
        data = [{
            'title': elem.a.div.contents[0].split('.')[1],
            'artist': str(elem.a.div.contents[1]).lstrip('<span>').rstrip(
                '</span>').strip(),
            'link': elem.a.get('href')
        } for elem in new_songs_wrapper]

        return data


class TooXclusiveClient(AbstractBaseClient):
    # This peoples yeye site was hard af to crawl. damn!
    def __init__(self):
        super(TooXclusiveClient, self).__init__(url='http://tooxclusive.com')

    def get_latest_songs(self):
        the_div = self._body.find(id='wpshower_popular_posts-9')
        data = []
        lis = the_div.contents[1].find_all('li')
        for li in lis:
            songs_data = dict()
            category = li.contents[3].a.text.lower()
            if category == 'audio':
                songs_data['title'] = li.contents[5].a.text
                songs_data['link'] = li.contents[5].a.get('href')

            data.append(songs_data)

        return data


class NotJustOkClient(AbstractBaseClient):
    # notjustok.com has an error in their html. A div class that closes wrongly.
    # This error affects results of the crawl. Nothing Icd.. can do about their
    # insubordination. we get data that way.
    def __init__(self):
        super(NotJustOkClient, self).__init__(url='https://notjustok.com/')

    def get_latest_songs(self):
        main_div = self._body.find(id='notjustok-posts')
        subs = [x for x in main_div.contents if x.name == 'article']
        data = []
        print(subs)
        for elem in subs:
            songs_data = dict()
            categories = elem.div.div.span.find_all('a')
            category_text = [x.text.lower() for x in categories]
            if 'music' in category_text:
                songs_data['title'] = elem.div.contents[3].span.a.text
                songs_data['link'] = elem.div.contents[3].span.a.get('href')
            else:
                continue

            data.append(songs_data)

        return data


if __name__ == '__main__':
    n = NaijaLoadedClient()
    print(n.get_latest_songs())

    # print(type(r'\n'))
