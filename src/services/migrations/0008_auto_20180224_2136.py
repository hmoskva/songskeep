# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-24 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20180223_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='site',
            field=models.ManyToManyField(blank=True, related_name='subscribed', to='services.Site'),
        ),
    ]
