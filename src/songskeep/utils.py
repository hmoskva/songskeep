import os
import random

from django.conf import settings
from songskeep.config import CONFIGS
from sparkpost import SparkPost

sp = SparkPost(api_key=CONFIGS['SPARKPOST_API_KEY'])


class Emailer:
    def __init__(self, **kwargs):
        self._recipients = kwargs.get('recipients')
        self._html = ''
        self._subject = ''
        self._type = kwargs.get('type')
        self._attempts = 1

    def send_email(self):
        self._clean_templates()
        try:
            response = sp.transmission.send(
                recipients=self._recipients,
                html=self._html,
                from_email=getattr(settings, 'FROM_EMAIL'),
                subject=self._subject,
                track_opens=True,
                track_clicks=True
            )
            return response
        except ConnectionError as e:
            print(e)
            self._attempts += 1
            self.send_email()
        except Exception as e:
            print(e)
        finally:
            print('Attempts at sending email: {}'.format(str(self._attempts)))

    def _clean_templates(self):
        if not self._type and not self._html:
            raise ValueError('Email type and html not being set')

        email_templates = getattr(settings, 'EMAIL_EXTRAS').get('type')
        if self._type in email_templates:
            self._subject = email_templates[self._type]['subject']
            self._html = email_templates[self._type]['html']


def get_filename_ext(filepath):
    """
        Method to split file path into corresponding name and extension
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    """
        Method to customize filename using random number and file extension
    """
    new_file_name = instance.name + '_' + str(random.randint(1, 9000))
    name, ext = get_filename_ext(filename)
    final_file_name = '{new_file_name}{ext}'.format(new_file_name=new_file_name, ext=ext)
    return 'sites/{new_file_name}/{final_file_name}'.format(
        new_file_name=new_file_name, final_file_name=final_file_name)







