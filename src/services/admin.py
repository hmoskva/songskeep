from django.contrib import admin

from .models import Site, Song, Subscription

admin.site.register(Site)
admin.site.register(Song)
admin.site.register(Subscription)
