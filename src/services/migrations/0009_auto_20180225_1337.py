# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-25 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20180224_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='site',
        ),
        migrations.AddField(
            model_name='subscription',
            name='category',
            field=models.CharField(default='naija', help_text='You will receive email notifications when new songs are added in category', max_length=120),
            preserve_default=False,
        ),
    ]
