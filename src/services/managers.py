from django.db import models


class SiteManager(models.Manager):
    def get_by_category(self, category):
        return self.get_queryset().filter(category=category, active=True)



