import os
import random

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from songskeep.utils import upload_image_path

from .managers import SiteManager


class Site(models.Model):
    OK = 'O'
    ERROR = 'E'
    RUNNING = 'R'

    CURRENT_STATUS_CHOICES = (
        (OK, 'Ok'),
        (ERROR, 'Error'),
        (RUNNING, 'Running')
    )
    CATEGORY_CHOICES = (('naija', 'Nigerian'), ('foreign', 'Foreign'))

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(null=True, blank=True)
    url = models.URLField()
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES)
    logo = models.ImageField(null=True, blank=True, upload_to=upload_image_path)
    active = models.BooleanField(default=True)
    status = models.CharField(choices=CURRENT_STATUS_CHOICES, max_length=1, default=OK)
    last_run = models.DateTimeField(null=True, blank=True)

    objects = SiteManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sites:songs', kwargs={'slug': self.slug})

    def get_archive_url(self):
        return reverse('sites:archive', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Site, self).save(*args, **kwargs)

    @property
    def props(self):
        if self.last_run:
            return 'Category: {}. Last run: {}'.format(self.category, self.last_run.date())
        return 'Category: {}. Last run: Not run yet'.format(self.category)

    class Meta:
        ordering = ('name',)


class Song(models.Model):
    title = models.CharField(max_length=120)
    artist = models.CharField(max_length=120, default='unavailable')
    site = models.ForeignKey(Site, related_name='songs')
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'song'
        verbose_name_plural = 'songs'


class Subscription(models.Model):
    email = models.EmailField(unique=True, primary_key=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
